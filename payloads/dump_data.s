# ================================================================================
# Copyright 2024 Antonio Porsia

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ================================================================================

# Dumps all data memory to UART

# Ugly hack to offset branches and align addresses with the start of the buffer.
# It generates a bunch of zeros that must be manually removed
.org 0x0006AC70

# Load UART starting address into a4
li a4, 0x200B0000
li t0, 0x40000
li t1, 0x80000

uart_put:
uart_wait_while_full:
    lw a5, 16(a4)
    andi a5, a5, 1
    bnez a5, uart_wait_until_full
    
    lb a2, 0(t0)
    sw a2, 24(a4)
uart_wait_until_idle:
    lw a5, 16(a4)
    srli a5, a5, 3

    # Here to avoid using beq, which for some reason the assembler substitues with a jump to address 0
    not a5, a5 
    andi a5, a5, 1
    bnez a5, uart_wait_until_idle
    
    addi t0, t0, 1
    bne t0, t1, uart_put
end:
    # Jump to bootrom
    li ra, 0x180
    jr ra
