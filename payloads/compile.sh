#!/bin/bash
RISCV=/tools/riscv/bin
RISCV_PREFIX=riscv32-unknown-elf

filename=$(basename -- "$1")
filename="${filename%.*}"
${RISCV}/${RISCV_PREFIX}-as -march=rv32imc -mno-arch-attr -fpic $1 -o ${filename}.elf
${RISCV}/${RISCV_PREFIX}-objcopy -O binary ${filename}.elf ${filename}.bin
xxd -ps -c 32768 ${filename}.bin > ${filename}.txt
if [ "$1" = "dump_data.s" ]; then
    tail -c 109 ${filename}.txt > ${filename}_data.txt
    mv ${filename}_data.txt ${filename}.txt
fi