# Variáveis do Projeto
PYTHON_FILE = stern_gerlach.py
SCRIPT_FILE = script.md
PIPELINE_FILE = narration_pipeline.py
MANIM_VIDEO_DIR = media/videos/stern_gerlach/1080p60
AUDIO_DIR = media/narration_audio
WORK_DIR = media/narration_work
FINAL_VIDEO = SternGerlach.mp4
PYTHON_BIN := $(if $(wildcard venv/bin/python),venv/bin/python,python3)
MANIM := $(PYTHON_BIN) -m manim
VOICE ?= pt-BR-AntonioNeural
RATE ?= -5%

.PHONY: all audio mux low scene1 scene2 scene3 scene4 clean

# Compilação padrão: renderiza os vídeos, gera a narração e entrega o arquivo final sincronizado.
all: mux

# Apenas compila a narração a partir de script.md.
audio:
	$(PYTHON_BIN) $(PIPELINE_FILE) audio --script $(SCRIPT_FILE) --audio-dir $(AUDIO_DIR) --voice=$(VOICE) --rate=$(RATE)

# Renderiza as cenas em alta qualidade, gera a voz e junta áudio e vídeo.
mux:
	$(MANIM) -qh $(PYTHON_FILE) -a
	$(PYTHON_BIN) $(PIPELINE_FILE) mux --script $(SCRIPT_FILE) --audio-dir $(AUDIO_DIR) --video-dir $(MANIM_VIDEO_DIR) --work-dir $(WORK_DIR) --output $(FINAL_VIDEO) --voice=$(VOICE) --rate=$(RATE)

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