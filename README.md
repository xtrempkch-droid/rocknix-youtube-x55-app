Como o X55 roda Linux e tem suporte a Python e MPV (player de vídeo), podemos criar um script simples que busca um vídeo e o toca.

O que você precisa:

    Acesso ao terminal do X55 (via SSH ou Terminal no dispositivo).

    Instalar a biblioteca yt-dlp (o padrão ouro para vídeos em Linux).

Passo 1: Instalar dependências (via Terminal/SSH)

Você precisará se conectar ao X55 via SSH (o usuário/senha padrão geralmente é root/linux ou root/jelos).
Bash

# Atualize o pip
pip install --upgrade pip

# Instale o yt-dlp (ferramenta que extrai o vídeo)
pip install yt-dlp


Como usar no X55

    Mapeamento de Botões: No sistema JELOS/ROCKNIX do X55, o D-Pad e os botões costumam ser mapeados para as setas do teclado e a tecla Enter.

        D-Pad Cima/Baixo: Navega na lista.

        Botão A: Seleciona/Aperta Enter.

        Botão Select/Start: Pode ser configurado para abrir a busca.

    Performance: O script usa o yt-dlp apenas para buscar informações leves. O vídeo pesado é processado pelo mpv, que no X55 é otimizado para o chip RK3566, garantindo que não trave.

   v2


    Como integrar no menu do JELOS/ROCKNIX

Para que ele apareça como um app real no seu console:

    Crie um script shell chamado YouTube.sh na pasta /storage/roms/ports/.

    Coloque o seguinte conteúdo:
    Bash

    #!/bin/bash
    python3 /caminho/para/seu/script/yt_tv.py

    Dê permissão de execução: chmod +x YouTube.sh.

Agora ele aparecerá na seção "Ports" do seu sistema operacional, pronto para ser jogado.


