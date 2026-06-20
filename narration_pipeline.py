from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


DEFAULT_SCENES = ["scene1", "scene2", "scene3", "scene4"]


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def run_ffprobe_duration(media_path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(media_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def find_audio_file(audio_dir: Path, scene_name: str) -> Path:
    candidates = [
        audio_dir / f"{scene_name}.mp3",
        audio_dir / f"{scene_name}.m4a",
        audio_dir / f"{scene_name}.wav",
        audio_dir / f"{scene_name.capitalize()}.mp3",
        audio_dir / f"{scene_name.capitalize()}.m4a",
        audio_dir / f"{scene_name.capitalize()}.wav",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"Não encontrei áudio para {scene_name}. Coloque o arquivo em {audio_dir} como {scene_name}.mp3."
    )


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
            "-b:a",
            "160k",
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
    concat_lines = [f"file '{video.resolve().as_posix()}'" for video in scene_videos]
    concat_list.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
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


def build_muxed_video(
    video_dir: Path,
    audio_dir: Path,
    work_dir: Path,
    final_output: Path,
    scenes: list[str] | None = None,
) -> None:
    ensure_directory(work_dir)
    muxed_dir = work_dir / "muxed"
    ensure_directory(muxed_dir)

    scene_names = scenes or DEFAULT_SCENES
    scene_video_paths: list[Path] = []

    for scene_name in scene_names:
        video_path = video_dir / f"Scene{scene_name[-1]}.mp4"
        if not video_path.exists():
            raise FileNotFoundError(f"Não encontrei o vídeo da cena em {video_path}")

        audio_input = find_audio_file(audio_dir, scene_name)
        target_duration = run_ffprobe_duration(video_path)
        fitted_audio = work_dir / f"{scene_name}_fitted.m4a"
        trim_or_pad_audio(audio_input, fitted_audio, target_duration)

        muxed_scene = muxed_dir / f"Scene{scene_name[-1]}.mp4"
        mux_scene(video_path, fitted_audio, muxed_scene)
        scene_video_paths.append(muxed_scene)

    concat_videos(scene_video_paths, final_output, work_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description="Mux manual de áudio para Stern-Gerlach.")
    parser.add_argument("--video-dir", type=Path, required=True, help="Diretório dos vídeos renderizados.")
    parser.add_argument("--audio-dir", type=Path, required=True, help="Diretório com scene1.mp3, scene2.mp3, etc.")
    parser.add_argument("--work-dir", type=Path, default=Path("media/manual_mux_work"), help="Diretório temporário.")
    parser.add_argument("--output", type=Path, default=Path("SternGerlach.mp4"), help="Arquivo final de vídeo com áudio.")
    args = parser.parse_args()

    build_muxed_video(
        video_dir=args.video_dir,
        audio_dir=args.audio_dir,
        work_dir=args.work_dir,
        final_output=args.output,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


if __name__ == "__main__":
    raise SystemExit(main())