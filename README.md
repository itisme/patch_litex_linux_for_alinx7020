## Other Languages

* [中文版](README_zh_CN.md)

# patch_litex_linux_for_alinx7020

Create and apply patches to the original litex and litex-boards packages to enable support for the Alinx7020 development board.

### Operation Instructions (Tested on Linux)

**Installation**

1. The simplest way to apply the patch is by cloning the `litex` project from https://github.com/itisme/litex and then installing it:
    - Install litex:
      ```bash
      git clone https://github.com/itisme/litex
      cd litex
      python ./litex_setup.py --init --install --user (--user to install to user directory) --config=(minimal, standard, full)
      ```
    - Compile a Linux test project based on the `alinx_ax7020` development board, which depends on the Vivado environment:
      ```bash
      git clone https://github.com/itisme/linux-on-litex-vexriscv
      source <Xilinx Vivado dir>/settings64.sh
      python ./make.py --board ax7020 --uart-baudrate 1e6 --build
      ```

2. Alternatively, clone the original `litex` repository, run the patch scripts for this project, and then compile the test program:
    - Install litex:
      ```bash
      git clone https://github.com/enjoy-digital/litex
      cd litex
      python ./litex_setup.py --init --install --user (--user to install to user directory) --config=(minimal, standard, full)
      ```
    - Apply patches:
      ```bash
      git clone https://github.com/itisme/patch_litex_linux_for_alinx7020
      cd patch_litex_linux_for_alinx7020
      python ./patch_litex.py
      python ./patch_litex-boards.py
      ```
    - Compile a Linux test project based on the `alinx_ax7020` development board, which depends on the Vivado environment:
      ```bash
      git clone https://github.com/itisme/linux-on-litex-vexriscv
      source <Xilinx Vivado dir>/settings64.sh
      python ./make.py --board ax7020 --uart-baudrate 1e6 --build
      ```

**Running Linux**

1. **Hardware Connections:**
   - FPGA Serial Connection:
     Refer to the Alinx 7020 user manual to connect the serial cable. Pin W19 of the chip is the PL output pin, connected to the input of the USB-to-serial adapter; pin W18 is the PL input pin, connected to the output of the USB-to-serial adapter.
   - Connect the JTAG cable properly.

2. **Download the System Image:**
   - Download the [image file](https://github.com/litex-hub/linux-on-litex-vexriscv/issues/164), extract it to a specified directory, e.g., `images/`.

3. **Open Terminal 1**, run the terminal program as the system console. Before running, confirm the FPGA serial port. In this example, `/dev/ttyUSB1` is used with a default baud rate of 1M:
   ```bash
   litex_term --images=images/boot.json --speed=1e6 /dev/ttyUSB1
   ```

4. **Open Terminal 2**, load the compiled `ps7_init.tcl` file located at `<linux-on-litex-vexriscv>/build/ax7020/gateware/ax7020.gen/sources_1/ip/Zynq/ps7_init.tcl`:
   - Start xsdb:
     ```bash
     source <Xilinx Vivado dir>/settings64.sh
     hw_server &
     xsdb
     ```
   - In the xsdb environment, run the following commands:
     ```tcl
     source <linux-on-litex-vexriscv>/build/ax7020/gateware/ax7020.gen/sources_1/ip/Zynq/ps7_init.tcl
     ps7_init
     ps7_post_config
     ```
   - Then load the bit file:
     ```tcl
     fpga -file <linux-on-litex-vexriscv>/build/ax7020/gateware/ax7020.bit
     ```

Under normal circumstances, you should see the following output:
![boot image](./linux_litex_alinx7020_boot.png)
