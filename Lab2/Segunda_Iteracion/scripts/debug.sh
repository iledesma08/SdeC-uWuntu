#!/usr/bin/env bash
set -euo pipefail

# ─── Directories ──────────────────────────────────────────────────────────────
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$ROOT_DIR/src"
DEBUG_DIR="$ROOT_DIR/debug"
BUILD_DIR="$ROOT_DIR/build"

# ─── Prepare ──────────────────────────────────────────────────────────────────
echo "👉 Creating build and debug directories…"
mkdir -p "$BUILD_DIR" "$DEBUG_DIR"

# ─── 1) Assemble your ASM with DWARF symbols ──────────────────────────────────
echo "1/2) Assembling convert.asm ➜ $BUILD_DIR/convert.o"
nasm -f elf32 -g -F dwarf \
     "$SRC_DIR/convert.asm" \
     -o "$BUILD_DIR/convert.o"

# ─── 2) Compile the C test harness + link with ASM object ────────────────────
#    Assumes you have debug/debug.c as your harness (see earlier example)
echo "2/2) Compiling debug/debug.c + linking ➜ $DEBUG_DIR/debug"
gcc -m32 -g -fno-omit-frame-pointer -no-pie \
    "$ROOT_DIR/debug/debug.c" \
    "$BUILD_DIR/convert.o" \
    -o "$DEBUG_DIR/debug"

# ─── Done ─────────────────────────────────────────────────────────────────────
echo "✅ Debug executable ready at: $DEBUG_DIR/debug"

gdb -tui ./debug/debug