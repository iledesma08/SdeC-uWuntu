#!/bin/bash

nasm -f elf64 convert.asm -o convert.o
gcc -fPIC -shared main.c convert.o -o main.so
