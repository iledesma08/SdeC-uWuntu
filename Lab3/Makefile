# Nombre de los programas
PRIMER = src/primer_codigo
SEGUNDO = src/segundo_codigo

# Carpeta de binarios
BIN = bin

# Herramientas
AS = as
LD = ld
OBJCOPY = objcopy
QEMU = qemu-system-i386
GDB = gdb

# Flags
ASFLAGS = --32
LDFLAGS = -m elf_i386 -T link.ld

# Targets por defecto
all: $(BIN)/primer_codigo.img $(BIN)/segundo_codigo.img

# Crear carpeta bin si no existe
$(BIN):
	mkdir -p $(BIN)

# Compilar primer código
$(BIN)/primer_codigo.o: $(PRIMER).s | $(BIN)
	$(AS) $(ASFLAGS) -o $@ $<

$(BIN)/primer_codigo.bin: $(BIN)/primer_codigo.o
	$(LD) $(LDFLAGS) -o $@ $<
	
$(BIN)/primer_codigo.img: $(BIN)/primer_codigo.bin
	$(OBJCOPY) -O binary $< $@

# Compilar segundo código
$(BIN)/segundo_codigo.o: $(SEGUNDO).s | $(BIN)
	$(AS) $(ASFLAGS) -o $@ $<

$(BIN)/segundo_codigo.bin: $(BIN)/segundo_codigo.o
	$(LD) $(LDFLAGS) -o $@ $<
	
$(BIN)/segundo_codigo.img: $(BIN)/segundo_codigo.bin
	$(OBJCOPY) -O binary $< $@

# Limpiar
clean:
	rm -rf $(BIN)

# Ejecutar primer código
run_primer: all
	$(QEMU) -drive format=raw,file=$(BIN)/primer_codigo.img

# Ejecutar segundo código
run_segundo: all
	$(QEMU) -drive format=raw,file=$(BIN)/segundo_codigo.img

# Debuggear el primer código
debug_primer: all
	$(QEMU) -drive format=raw,file=$(BIN)/primer_codigo.img -S -gdb tcp::1234 -monitor stdio &
	sleep 1
	$(GDB) -ex "set architecture i8086" \
	       -ex "target remote localhost:1234" \
	       -ex "break *0x7c00" \
	       -ex "info registers" \
	       -ex "continue"

# Debuggear el segundo código
debug_segundo: all
	$(QEMU) -drive format=raw,file=$(BIN)/segundo_codigo.img -S -gdb tcp::1234 -monitor stdio &
	sleep 1
	$(GDB) -ex "set architecture i8086" \
	       -ex "target remote localhost:1234" \
	       -ex "break *0x7c00" \
	       -ex "info registers" \
	       -ex "continue"
