# Variáveis do Projeto
PYTHON_FILE = stern_gerlach.py

.PHONY: all low scene1 scene2 scene3 scene4 clean

# Compilação padrão (todas as cenas juntas em alta resolução e concatenação via ffmpeg)
all:
	manim -qh $(PYTHON_FILE) -a
	@echo "Concatenando as saídas em alta resolução..."
	@echo "file 'media/videos/stern_gerlach/1080p60/Scene1.mp4'" > concat.txt
	@echo "file 'media/videos/stern_gerlach/1080p60/Scene2.mp4'" >> concat.txt
	@echo "file 'media/videos/stern_gerlach/1080p60/Scene3.mp4'" >> concat.txt
	@echo "file 'media/videos/stern_gerlach/1080p60/Scene4.mp4'" >> concat.txt
	ffmpeg -f concat -safe 0 -i concat.txt -c copy SternGerlach.mp4
	@rm concat.txt

# Compilação de todas as cenas estruturadas em baixa resolução (Low Quality)
low:
	manim -ql $(PYTHON_FILE) -a

# Compilação individual de cenas em baixa resolução
scene1:
	manim -ql $(PYTHON_FILE) Scene1

scene2:
	manim -ql $(PYTHON_FILE) Scene2 

scene3:
	manim -ql $(PYTHON_FILE) Scene3

scene4:
	manim -ql $(PYTHON_FILE) Scene4

# Limpeza dos arquivos temporários e diretórios de mídia gerados
clean:
	rm -rf media/
	rm -f concat.txt SternGerlach.mp4