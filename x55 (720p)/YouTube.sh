#!/bin/bash

# Detecta o caminho base (X55 costuma usar /storage/roms ou /roms)
if [ -d "/storage/roms" ]; then
    BASE_PATH="/storage/roms"
else
    BASE_PATH="/roms"
fi

SCRIPT_PATH="$BASE_PATH/ports/scripts/yt_x55.py"
PYTHON_BIN="python3"

# Limpa a tela do terminal para uma interface limpa
clear
echo "--- X55 YOUTUBE SYSTEM CHECK ---"

# 1. Verifica Internet
wget -q --spider http://google.com
if [ $? -eq 0 ]; then
    echo "[OK] Conectado. Verificando atualizacoes..."
    
    # Instala/Atualiza yt-dlp e Textual silenciosamente
    $PYTHON_BIN -m pip install --upgrade pip &> /dev/null
    $PYTHON_BIN -m pip install yt-dlp textual &> /dev/null
    echo "[OK] Componentes atualizados."
else
    echo "[!] Offline: Pulando atualizacoes."
fi

# 2. Configurações de GPU para o Chip RK3566 do X55
export SDL_VIDEODRIVER=kmsdrm
export MESA_GL_VERSION_OVERRIDE=3.3

# 3. Executa o App
echo "Iniciando interface..."
$PYTHON_BIN $SCRIPT_PATH
