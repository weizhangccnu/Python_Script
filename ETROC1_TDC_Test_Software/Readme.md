## 1. This python script is used for testing the ETROC1 TDC chip
  - command_interpret.py is a class for sockect communication
  - kc705_mig_control.py includes all kinds of function such as I2C write/read, DDR3 data storage, Ethernet communication.
## 2. Hardware platform
  - The FPGA is Xilinx kc705 EVB and the FPGA socket address is 192.168.2.x, The x is configurable via switch (SW11, Pin1 and Pin2) and the value ranges from 0 to 3.
  - The python script is running on the Windows operating system.
  - Between the PC and KC705 EVB is connected by Ethernet cable. 
## 3. Software version
  - Firmware compliled on Vivado 2016.2 version
  - Python script should be executed on python3.7.5
  - Ethernet communication speed is 1Gbps, Please make sure the Ethernet cable can meet the requirements.

