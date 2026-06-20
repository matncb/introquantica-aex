# Variáveis do Projeto
PYTHON_FILE = stern_gerlach.py
SCRIPT_FILE = script.md
PIPELINE_FILE = narration_pipeline.py
MANIM_VIDEO_DIR = media/videos/stern_gerlach/1080p60
AUDIO_DIR = manual_audio
WORK_DIR = media/manual_mux_work
FINAL_VIDEO = SternGerlach.mp4
PYTHON_BIN := $(if $(wildcard venv/bin/python),venv/bin/python,python3)
MANIM := $(PYTHON_BIN) -m manim

.PHONY: all mux low scene1 scene2 scene3 scene4 clean

# Compilação padrão: renderiza os vídeos e junta os áudios manuais ao vídeo final.
all: mux

# Renderiza as cenas em alta qualidade e junta os áudios manuais scene1.mp3 etc.
mux:
	$(MANIM) -qh $(PYTHON_FILE) -a
	$(PYTHON_BIN) $(PIPELINE_FILE) --video-dir $(MANIM_VIDEO_DIR) --audio-dir $(AUDIO_DIR) --work-dir $(WORK_DIR) --output $(FINAL_VIDEO)

# Compilação de todas as cenas estruturadas em baixa resolução (Low Quality)
low:
	$(MANIM) -ql $(PYTHON_FILE) -a

# Compilação individual de cenas em baixa resolução
scene1:
	$(MANIM) -ql $(PYTHON_FILE) Scene1

scene2:
	$(MANIM) -ql $(PYTHON_FILE) Scene2 

scene3:
	$(MANIM) -ql $(PYTHON_FILE) Scene3

scene4:
	$(MANIM) -ql $(PYTHON_FILE) Scene4

# Limpeza dos arquivos temporários e diretórios de mídia gerados
clean:
	rm -rf media/
	rm -f $(FINAL_VIDEO)