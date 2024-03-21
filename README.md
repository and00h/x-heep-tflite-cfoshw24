# X-HEEP + Tensorflow Lite for Microcontrollers + Vulnerable app

This repository contains material related to the submission for the 2nd Workshop on Open-Source Hardware at the Computing Frontiers 2024 conference.

## Setup

### 1. Clone the repository on the Pynq-Z2
```bash
git clone --recurse-submodules https://github.com/and00h/x-heep-tflite-cfoshw24
```

### 2. Rename the SDK submodule
```bash
mv x-heep-femu-tflite-sdk x-heep-femu-sdk
```

### 3. Setup X-HEEP
Follow the instructions inside the X-HEEP FEMU SDK's [README](./x-heep-femu-tflite-sdk/README.md) to setup the Linux environment on the Pynq-Z2.

*Note: from now on, every command must be run on the Pynq board as the root user!*

Once the setup is complete and you have a working Linux environment on the Pynq, inside the `/home/xilinx` directory run:
```bash
source ./x-heep-femu-sdk/init.sh
```

### 4. Compile and run the vulnerable application
Open a python shell by running `python3` and type:

```python
from pynq import x_heep
x = x_heep()
x.compile_app("tflite_scpi")
x.run_app()
```

To verify that everything is working, check the output on the UART port:

```bash
screen -r uart
```

After a few seconds, some output should appear and you should be able to type commands.

*Beware that it is not possible to delete characters, so if you type a wrong command just press enter, the application should give you an error and wait for another command*

Once everything is working, press `Ctrl+A` then `Ctrl+D` to exit `screen`.

#### Compile TFLM
Note that compiling the Tensorflow Lite for Microcontrollers library will take a long time if done directly on the Pynq. To speed up the process, you can mount the Pynq's home folder on another machine where you have installed the RISC-V toolchain following the instructions in [X-HEEP's repository]((https://github.com/esl-epfl/x-heep)) and compile TFLM from there.

For example you can run (**on another machine, not on the Pynq**):

```bash
mkdir pynq && sshfs xilinx@<pynq ip>:/home/xilinx pynq
```

And then run `make`:

```bash
cd pynq/x-heep-femu-sdk 

make -j4 -C sw/riscv/lib/tflite-micro RISCV=/path/to/riscv/toolchain/on/your/machine X_HEEP_LIB_FOLDER=../../lib
```

### 5. Compile and send the payloads
While the app is running on X-HEEP, open another shell as the root user on the board and run

```bash
source ./x-heep-femu-sdk/init.sh
```

Then `cd` into the `payloads` folder.

#### Find start of buffer
Run:

```bash
python3 find_start_of_buffer.py <hex-address-to-start-looking-from>
```

Note that X-HEEP may freeze since we are jumping to random locations in memory. If it happens, just repeat step 4 and restart the script using the address that froze X-HEEP minus `0x200`.

#### Dump data memory
Run:

```bash
python3 dump_data.py <buffer_address_found_with_the_previous_script>
```

When the script terminates, the memory dump will be inside `x_heep_uart_dump.bin`. To recover the model, open the dump with an hex editor and search for the "TFL3" string. Starting 4 bytes before "TFL3", copy everything that comes after into another file (you can also stop before the end if you can identify the end of the model's data) and you're good to go, you can load your stolen model with TFLM!

#### Custom payload

You can use the `send_payload.py` script to compile and send custom payloads to the vulnerable application. 
