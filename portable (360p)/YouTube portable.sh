#!/bin/bash

# Caminho para o ambiente virtual ou python do sistema
PYTHON_BIN="python3"
SCRIPT_PATH="/roms/ports/scripts/yt_portable.py" # Ajuste para o seu caminho real

echo "Iniciando verificacoes do sistema..."

# 1. Verifica se existe conexão com a internet
wget -q --spider http://google.com
if [ $? -eq 0 ]; then
    echo "Internet detectada. Verificando yt-dlp..."
    
    # 2. Verifica se o yt-dlp está instalado
    if ! command -v yt-dlp &> /dev/null; then
        echo "yt-dlp nao encontrado. Instalando..."
        $PYTHON_BIN -m pip install yt-dlp
    else
        echo "yt-dlp ja instalado. Atualizando para evitar erros..."
        # Atualiza em segundo plano para nao demorar a abertura
        $PYTHON_BIN -m pip install -U yt-dlp & 
    fi

    # 3. Verifica a biblioteca Textual (interface)
    if ! $PYTHON_BIN -c "import textual" &> /dev/null; then
        echo "Instalando biblioteca de interface (Textual)..."
        $PYTHON_BIN -m pip install textual
    fi
else
    echo "Sem internet. Tentando abrir o app em modo offline..."
fi

# 4. Executa o script do YouTube
echo "Abrindo o YouTube..."
$PYTHON_BIN $SCRIPT_PATH
