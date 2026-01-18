#!/usr/bin/env bash
# Chame o script Python principal a partir do diretório onde o script está localizado.
# Torne este arquivo executável: chmod +x YouTube.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "${SCRIPT_DIR}/yt_tv.py"
