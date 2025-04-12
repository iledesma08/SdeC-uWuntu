#!/bin/bash
set -e  

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$ROOT_DIR/src"
VENV_DIR="$ROOT_DIR/venv"
LIB_NAME="main.so"

echo "[1/5] Creating Python virtual environment..."

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
echo "Virtual environment activated."

echo "[2/5] Installing Python dependencies..."
pip install --upgrade pip
pip install flask requests matplotlib numpy plotly
echo "Dependencies installed."

echo "[3/5] Compiling assembler..."
nasm -f elf64 "$SRC_DIR/convert.asm" -o "$SRC_DIR/convert.o"

echo "[4/5] Compiling and linking C + ASM into $LIB_NAME..."
gcc -fPIC -shared "$SRC_DIR/main.c" "$SRC_DIR/convert.o" -o "$SRC_DIR/$LIB_NAME"

echo "[5/5] Build complete. Shared library created at: $SRC_DIR/$LIB_NAME"
ls -lh "$SRC_DIR/$LIB_NAME"

echo ""
echo "Todo listo. Para iniciar tu aplicación Flask:"
echo ""
echo "./scripts/run.sh"
echo ""
echo "Asegurate de que tenga permisos de ejecución:"
echo "chmod +x scripts/run_flask.sh"
echo ""
echo "Una vez iniciada, accedé en tu navegador a:"
echo "http://localhost:5000"