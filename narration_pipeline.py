from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
from pathlib import Path


SCENE_PATTERN = re.compile(r"^##\s+Cena\s+(\d+)\s*$", re.MULTILINE)


def parse_script(script_path: Path) -> dict[str, str]:
    content = script_path.read_text(encoding="utf-8")
    matches = list(SCENE_PATTERN.finditer(content))
    if not matches:
        raise ValueError("O script precisa ter blocos com títulos no formato '## Cena 1'.")

    scenes: dict[str, str] = {}
    for index, match in enumerate(matches):
        scene_number = match.group(1)
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        scene_body = content[start:end].strip()
        scene_body = cleanup_text(scene_body)
        if not scene_body:
            raise ValueError(f"A cena {scene_number} está vazia no roteiro.")
        scenes[f"Scene{scene_number}"] = scene_body
    return scenes


def cleanup_text(text: str) -> str:
    text = re.sub(r"^\s*#+\s*", "", text, flags=re.MULTILINE)
    text = text.replace("**", "")
    text = text.replace("$", "")
    text = text.replace("`", "")
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


async def synthesize_audio(scene_name: str, text: str, output_path: Path, voice: str, rate: str) -> None:
    import edge_tts

    communicator = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicator.save(str(output_path))


def voice_candidates(preferred_voice: str) -> list[str]:
    fallback_order = [preferred_voice, "pt-BR-FranciscaNeural", "pt-BR-AntonioNeural"]
    unique_candidates: list[str] = []
    for candidate in fallback_order:
        if candidate not in unique_candidates:
            unique_candidates.append(candidate)
    return unique_candidates


async def synthesize_audio_with_fallback(
    scene_name: str,
    text: str,
    output_path: Path,
    preferred_voice: str,
    rate: str,
) -> str:
    last_error: Exception | None = None
    for candidate_voice in voice_candidates(preferred_voice):
        try:
            await synthesize_audio(scene_name, text, output_path, candidate_voice, rate)
            if candidate_voice != preferred_voice:
                print(f"[{scene_name}] voz alternativa aplicada: {candidate_voice}")
            return candidate_voice
        except Exception as exc:
            last_error = exc
    assert last_error is not None
    raise last_error


def run_ffprobe_duration(video_path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(video_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def trim_or_pad_audio(input_path: Path, output_path: Path, duration: float) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(input_path),
            "-af",
            f"apad,atrim=duration={duration:.3f}",
            "-ac",
            "2",
            "-ar",
            "48000",
            "-c:a",
            "aac",
            str(output_path),
        ],
        check=True,
    )


def mux_scene(video_path: Path, audio_path: Path, output_path: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-i",
            str(audio_path),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            "-shortest",
            str(output_path),
        ],
        check=True,
    )


def concat_videos(scene_videos: list[Path], output_path: Path, work_dir: Path) -> None:
    concat_list = work_dir / "concat.txt"
    lines = [f"file '{scene.resolve().as_posix()}'" for scene in scene_videos]
    concat_list.write_text("\n".join(lines) + "\n", encoding="utf-8")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c",
            "copy",
            str(output_path),
        ],
        check=True,
    )


async def generate_audio_assets(script_path: Path, audio_dir: Path, voice: str, rate: str) -> dict[str, Path]:
    scenes = parse_script(script_path)
    ensure_directory(audio_dir)

    generated: dict[str, Path] = {}
    for scene_name, text in scenes.items():
        raw_audio = audio_dir / f"{scene_name}.mp3"
        await synthesize_audio_with_fallback(scene_name, text, raw_audio, voice, rate)
        generated[scene_name] = raw_audio
    return generated


def build_muxed_video(
    script_path: Path,
    audio_dir: Path,
    video_dir: Path,
    work_dir: Path,
    final_output: Path,
    voice: str,
    rate: str,
) -> None:
    scenes = parse_script(script_path)
    ensure_directory(audio_dir)
    ensure_directory(work_dir)

    raw_audio_dir = audio_dir
    adjusted_audio_dir = work_dir / "adjusted_audio"
    muxed_dir = work_dir / "muxed"
    ensure_directory(raw_audio_dir)
    ensure_directory(adjusted_audio_dir)
    ensure_directory(muxed_dir)

    scene_video_paths: list[Path] = []

    async def _generate() -> None:
        for scene_name, text in scenes.items():
            raw_audio = raw_audio_dir / f"{scene_name}.mp3"
            await synthesize_audio_with_fallback(scene_name, text, raw_audio, voice, rate)
            duration = run_ffprobe_duration(video_dir / f"{scene_name}.mp4")
            adjusted_audio = adjusted_audio_dir / f"{scene_name}.m4a"
            trim_or_pad_audio(raw_audio, adjusted_audio, duration)

            muxed_scene = muxed_dir / f"{scene_name}.mp4"
            mux_scene(video_dir / f"{scene_name}.mp4", adjusted_audio, muxed_scene)
            scene_video_paths.append(muxed_scene)

    asyncio.run(_generate())
    concat_videos(scene_video_paths, final_output, work_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description="Pipeline de narração e mux para Stern-Gerlach.")
    parser.add_argument("mode", choices=("audio", "mux"), help="Modo de execução.")
    parser.add_argument("--script", type=Path, required=True, help="Arquivo markdown com o roteiro.")
    parser.add_argument("--audio-dir", type=Path, required=True, help="Diretório de saída do áudio.")
    parser.add_argument("--video-dir", type=Path, help="Diretório dos vídeos renderizados.")
    parser.add_argument("--work-dir", type=Path, default=Path("media/narration_work"), help="Diretório temporário.")
    parser.add_argument("--output", type=Path, help="Arquivo final de vídeo com áudio.")
    parser.add_argument("--voice", default="pt-BR-ThalitaMultilingualNeural", help="Voz neural do edge-tts.")
    parser.add_argument("--rate", default="-5%", help="Velocidade da fala.")
    args = parser.parse_args()

    if args.mode == "audio":
        asyncio.run(generate_audio_assets(args.script, args.audio_dir, args.voice, args.rate))
        return 0

    if args.video_dir is None:
        parser.error("--video-dir é obrigatório no modo mux.")
    if args.output is None:
        parser.error("--output é obrigatório no modo mux.")

    build_muxed_video(
        script_path=args.script,
        audio_dir=args.audio_dir,
        video_dir=args.video_dir,
        work_dir=args.work_dir,
        final_output=args.output,
        voice=args.voice,
        rate=args.rate,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())