#!/bin/bash

# Cores
GREEN='\033[0;32m'
NC='\033[0m'

echo "Iniciando instalacao do YouTube App..."

# 1. Detecta o sistema de arquivos (X55 vs R36S)
if [ -d "/storage/roms" ]; then
    BASE="/storage/roms" # JELOS / ROCKNIX
else
    BASE="/roms" # ArkOS / AmberELEC
fi

# 2. Define caminhos
PORT_DIR="$BASE/ports"
SCRIPT_DIR="$PORT_DIR/scripts"

# 3. Cria pastas
mkdir -p "$SCRIPT_DIR"

# 4. Download dos arquivos (apontando para o seu repo)
echo "Baixando arquivos..."
curl -L "https://raw.githubusercontent.com/xtrempkch-droid/rocknix-youtube-x55-app/main/yt_x55.py" -o "$SCRIPT_DIR/yt_app.py"
curl -L "https://raw.githubusercontent.com/xtrempkch-droid/rocknix-youtube-x55-app/main/YouTube.sh" -o "$PORT_DIR/YouTube.sh"

# 5. Permissões
chmod +x "$PORT_DIR/YouTube.sh"

# 6. Dependências
echo "Instalando dependencias..."
python3 -m pip install yt-dlp textual

echo -e "${GREEN}Pronto! O app foi instalado em $PORT_DIR/YouTube.sh${NC}"
