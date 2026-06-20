# Stern-Gerlach com Manim e narração sincronizada

Este projeto produz um vídeo de divulgação científica sobre o experimento de Stern-Gerlach com quatro cenas em Manim e narração gerada a partir de um roteiro em Markdown.

## O que o projeto faz

- Renderiza as quatro cenas definidas em [stern_gerlach.py](stern_gerlach.py).
- Lê o roteiro em [script.md](script.md) e divide a narração por cena usando os blocos `## Cena 1`, `## Cena 2`, `## Cena 3` e `## Cena 4`.
- Gera áudio com a biblioteca `edge-tts`, buscando uma voz neural em português.
- Ajusta cada faixa de áudio à duração do vídeo correspondente e entrega um arquivo final já sincronizado.

## Dependências

Você precisa de:

- Python 3 com ambiente virtual local em `venv/`.
- `ffmpeg` e `ffprobe` instalados no sistema.
- As bibliotecas Python listadas em [requirements.txt](requirements.txt).

Se o ambiente ainda não estiver pronto, crie e instale as dependências com:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Como usar

O fluxo principal é:

```bash
make all
```

Esse comando faz três coisas em sequência:

1. Renderiza as cenas do Manim em alta qualidade.
2. Gera a narração por cena a partir de [script.md](script.md).
3. Junta áudio e vídeo e salva o resultado em `SternGerlach.mp4`.

Se você quiser apenas gerar a narração, sem renderizar o vídeo:

```bash
make audio
```

Se quiser apenas renderizar e depois fazer a junção final:

```bash
make mux
```

## Alvos do Makefile

- `make all`: fluxo completo, equivalente a renderizar, narrar e muxar.
- `make mux`: renderização em alta qualidade e junção final com áudio.
- `make audio`: gera apenas os arquivos de áudio por cena.
- `make low`: renderiza todas as cenas em baixa qualidade, sem narração.
- `make scene1`, `make scene2`, `make scene3`, `make scene4`: renderizam cenas isoladas.
- `make clean`: remove a pasta `media/` e o vídeo final.

## Como o áudio é sincronizado

O pipeline de narração lê o texto de [script.md](script.md), sintetiza cada cena separadamente e compara a duração do áudio com a duração do vídeo renderizado daquela cena. Depois disso, ele ajusta o áudio com `ffmpeg` para casar com o tempo do vídeo antes de fazer o mux.

Isso deixa a sincronização mais segura porque cada cena é tratada individualmente, reduzindo o risco de um trecho ficar adiantado ou atrasado quando o texto mudar.

## Voz e velocidade

Por padrão, o projeto usa:

- Voz: `pt-BR-AntonioNeural`
- Velocidade: `-5%`

Você pode alterar isso sem mexer no código:

```bash
make all VOICE=pt-BR-AntonioNeural RATE=-10%
```

## Estrutura importante

- [stern_gerlach.py](stern_gerlach.py): cenas e animações.
- [script.md](script.md): roteiro da narração.
- [narration_pipeline.py](narration_pipeline.py): geração de voz e mux final.
- [makefile](makefile): comandos de compilação.

## Saídas geradas

- `media/narration_audio/`: áudio bruto por cena.
- `media/narration_work/`: arquivos intermediários de ajuste e mux.
- `media/videos/stern_gerlach/1080p60/`: vídeos renderizados pelo Manim.
- `SternGerlach.mp4`: vídeo final com áudio sincronizado.

## Observações práticas

- Se você editar [script.md](script.md), rode `make audio` ou `make all` novamente para regenerar a narração.
- Se mudar o conteúdo visual em [stern_gerlach.py](stern_gerlach.py), rode `make all` para que o áudio seja alinhado com o novo tempo de cada cena.
- Se o `make all` falhar por falta de `ffmpeg`, `ffprobe` ou dependências Python, instale essas ferramentas antes de tentar de novo.