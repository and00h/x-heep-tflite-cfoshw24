# X-HEEP + Tensorflow Lite for Microcontrollers + Vulnerable app

This repository contains material related to the submission for the 2nd Workshop on Open-Source Hardware.

## Setup

### 1. Clone the repository on the Pynq-Z2
```bash
git clone --recurse-submodules https://github.com/and00h/x-heep-tflite-cfoshw24
```

### 2. Rename the SDK submodule
```bash
mv x-heep-tflite-cfoshw24 x-heep-femu-sdk
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

### 5. Compile and send the payloads
While the app is running on X-HEEP, open another shell as the root user on the board, run

```bash
source ./x-heep-femu-sdk/init.sh
```

and `cd` into the `payloads` folder.

#### Find start of buffer
Run:

```bash
python3 find_start_of_buffer.py <hex-address-to-start-looking-from>
```

Note that X-HEEP may freeze since we are jumping to random locations in memory. If it happens, just repeat step 4 and restart the script using the address that froze X-HEEP minus `0x200`.

#### Dump data memory
Run:

```bash
python3 dump_data.py
```

When the script terminates, the dumped data will be inside the file `x_heep_uart_dump.bin`.

#### Custom payload

You can use the `send_payload.py` script to compile and send custom payloads to the vulnerable application. 