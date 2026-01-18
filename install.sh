#!/bin/bash
# INSTALADOR OFICIAL ROCKNIX-YOUTUBE-X55

if [ -d "/storage/roms" ]; then
    BASE="/storage/roms"
else
    BASE="/roms"
fi

PORT_DIR="$BASE/ports"
SCRIPT_DIR="$PORT_DIR/scripts"

mkdir -p "$SCRIPT_DIR"

echo "A descarregar ficheiros do repositório..."

# ATENÇÃO: Aqui usamos o nome yt_x55.py que é o que está no teu GitHub
curl -L "https://raw.githubusercontent.com/xtrempkch-droid/rocknix-youtube-x55-app/main/yt_x55.py" -o "$SCRIPT_DIR/yt_x55.py"
curl -L "https://raw.githubusercontent.com/xtrempkch-droid/rocknix-youtube-x55-app/main/YouTube.sh" -o "$PORT_DIR/YouTube.sh"

chmod +x "$PORT_DIR/YouTube.sh"

echo "A instalar dependências..."
python3 -m pip install yt-dlp textual

echo "Instalação concluída! Reinicia o EmulationStation."
