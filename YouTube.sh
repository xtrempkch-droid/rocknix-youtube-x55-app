#!/bin/bash

# ==========================================================
# LAUNCHER UNIVERSAL YOUTUBE (X55 & R36S)
# ==========================================================

# 1. Detectar o caminho base do sistema
if [ -d "/storage/roms" ]; then
    # Caminho padrão JELOS / ROCKNIX (X55)
    BASE_PATH="/storage/roms"
else
    # Caminho padrão ArkOS / AmberELEC (R36S)
    BASE_PATH="/roms"
fi

# 2. Definir caminhos dos arquivos
SCRIPT_PATH="$BASE_PATH/ports/scripts/yt_app.py"
PYTHON_BIN="python3"

clear
echo "------------------------------------------"
echo "        INICIANDO YOUTUBE PORTABLE        "
echo "------------------------------------------"

# 3. Verificação de Internet e Auto-Update
wget -q --spider http://google.com
if [ $? -eq 0 ]; then
    echo "[OK] Internet detectada. Verificando atualizacoes..."
    # Atualiza o yt-dlp em background para não atrasar o início
    $PYTHON_BIN -m pip install -U yt-dlp &>/dev/null &
    echo "[OK] Otimizacoes de rede aplicadas."
else
    echo "[!] Modo Offline: Verifique seu Wi-Fi."
fi

# 4. Configurações de GPU para Rockchip (RK3566/RK3326)
export SDL_VIDEODRIVER=kmsdrm
export MESA_GL_VERSION_OVERRIDE=3.3

# 5. Executar o Aplicativo
if [ -f "$SCRIPT_PATH" ]; then
    echo "Abrindo interface..."
    $PYTHON_BIN "$SCRIPT_PATH"
else
    echo "ERRO: Script nao encontrado em:"
    echo "$SCRIPT_PATH"
    echo "Por favor, execute o install.sh novamente."
    sleep 5
fi
