#!/bin/bash

set -e 

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

SRC_DIR="$SCRIPT_DIR/../src"
OUTPUT_DIR="$SCRIPT_DIR"

MAIN_S="$SRC_DIR/main.s"
LINKER_SCRIPT="$SRC_DIR/link.ld"
OBJ_FILE="$OUTPUT_DIR/main.o"
IMG_FILE="$OUTPUT_DIR/main.img"

echo "Assembling..."
as -g -o "$OBJ_FILE" "$MAIN_S"

echo "Linking..."
ld --oformat binary -o "$IMG_FILE" -T "$LINKER_SCRIPT" "$OBJ_FILE"

echo "Running in QEMU..."
qemu-system-x86_64 -drive format=raw,file="$IMG_FILE"

