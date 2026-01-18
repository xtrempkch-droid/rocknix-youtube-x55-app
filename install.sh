#!/bin/bash

# Cores para o terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # Sem cor

echo -e "${BLUE}===========================================${NC}"
echo -e "${GREEN}   Instalador YouTube App para X55 / R36S  ${NC}"
echo -e "${BLUE}===========================================${NC}"

# 1. Detectar o caminho das ROMS (X55 usa /storage, R36S usa /roms)
if [ -d "/storage/roms" ]; then
    ROM_PATH="/storage/roms"
else
    ROM_PATH="/roms"
fi

PORTS_PATH="$ROM_PATH/ports"
SCRIPTS_PATH="$PORTS_PATH/scripts"

echo -e "-> Detectado caminho de Ports em: $PORTS_PATH"

# 2. Criar diretórios se não existirem
mkdir -p "$SCRIPTS_PATH"

# 3. Baixar os arquivos do seu repositório GitHub
echo -e "-> Baixando arquivos do repositório..."
# Substitua pelo link 'raw' correto do seu GitHub
curl -sL "https://raw.githubusercontent.com/xtrempkch-droid/rocknix-youtube-x55-app/main/yt_x55.py" -o "$SCRIPTS_PATH/yt_x55.py"
curl -sL "https://raw.githubusercontent.com/xtrempkch-droid/rocknix-youtube-x55-app/main/YouTube.sh" -o "$PORTS_PATH/YouTube.sh"

# 4. Dar permissões de execução
chmod +x "$PORTS_PATH/YouTube.sh"

# 5. Instalar dependências Python
echo -e "-> Instalando dependências (yt-dlp e Textual)..."
python3 -m pip install --upgrade pip
python3 -m pip install yt-dlp textual

echo -e "${GREEN}===========================================${NC}"
echo -e "      INSTALAÇÃO CONCLUÍDA COM SUCESSO!     "
echo -e "   Reinicie o EmulationStation para ver o   "
echo -e "      app na sua lista de Ports.            "
echo -e "${GREEN}===========================================${NC}"
