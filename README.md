# Stern-Gerlach com Manim e áudio manual

Este projeto produz um vídeo de divulgação científica sobre o experimento de Stern-Gerlach com quatro cenas em Manim e áudio gravado manualmente por cena.

## O que o projeto faz

- Renderiza as quatro cenas definidas em [stern_gerlach.py](stern_gerlach.py).
- Você grava manualmente `scene1.mp3`, `scene2.mp3`, `scene3.mp3` e `scene4.mp3` em `media/manual_audio/`.
- O comando de mux ajusta cada áudio à duração da cena correspondente antes de juntar tudo no arquivo final.

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
2. Lê `media/manual_audio/scene1.mp3` até `scene4.mp3`.
3. Junta áudio e vídeo e salva o resultado em `SternGerlach.mp4`.

Se quiser apenas juntar os áudios manuais com o vídeo renderizado:

```bash
make mux
```

## Alvos do Makefile

- `make all`: fluxo completo, equivalente a renderizar e muxar.
- `make mux`: renderização em alta qualidade e junção final com áudio manual.
- `make low`: renderiza todas as cenas em baixa qualidade, sem narração.
- `make scene1`, `make scene2`, `make scene3`, `make scene4`: renderizam cenas isoladas.
- `make clean`: remove a pasta `media/` e o vídeo final.

## Onde colocar o áudio

Coloque os arquivos em `media/manual_audio/` com estes nomes:

- `scene1.mp3`
- `scene2.mp3`
- `scene3.mp3`
- `scene4.mp3`

O script de mux aceita também `m4a` e `wav`, mas o protótipo do projeto usa `mp3`.

O mux lê a duração de cada cena renderizada, ajusta o áudio manual daquela cena com `ffmpeg` e depois une o par cena-aúdio. Isso mantém a sincronização estável mesmo que o áudio gravado tenha pequenas diferenças de duração.

## Voz e velocidade

Não há mais geração automática de voz.

## Estrutura importante

- [stern_gerlach.py](stern_gerlach.py): cenas e animações.
- [script.md](script.md): roteiro da narração.
- [narration_pipeline.py](narration_pipeline.py): geração de voz e mux final.
- [makefile](makefile): comandos de compilação.

## Saídas geradas

- `manual_audio/`: áudio gravado manualmente por cena.
- `media/manual_mux_work/`: arquivos intermediários de ajuste e mux.
- `media/videos/stern_gerlach/1080p60/`: vídeos renderizados pelo Manim.
- `SternGerlach.mp4`: vídeo final com áudio sincronizado.

## Observações práticas

- Se você gravar novamente algum áudio, substitua o arquivo correspondente em `media/manual_audio/` e rode `make mux`.
- Se mudar o conteúdo visual em [stern_gerlach.py](stern_gerlach.py), rode `make all` para que os áudios sejam alinhados com o novo tempo de cada cena.
- Se o `make all` falhar por falta de `ffmpeg`, `ffprobe` ou dependências Python, instale essas ferramentas antes de tentar de novo.