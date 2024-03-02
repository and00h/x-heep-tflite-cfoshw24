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

# Load first canary into s4
li s4, 0x44434241

# NOP slide with second canary load into s3
.rept 59
nop
nop
nop
nop
li s3, 0x43414341
.endr

nop # Just for padding

# Load UART address
li a4, 0x200B0000

# Print content of s3 to UART
mv t1, s3
sw t1, 24(a4)
srl t1, t1, 8
sw t1, 24(a4)
srl t1, t1, 8
sw t1, 24(a4)
srl t1, t1, 8
sw t1, 24(a4)

# Print content of s4 to UART
mv t0, s4
sw t0, 24(a4)
srl t0, t0, 8
sw t0, 24(a4)
srl t0, t0, 8
sw t0, 24(a4)
srl t0, t0, 8
sw t0, 24(a4)

# Jump to bootrom
li ra, 0x180
jr ra
