## 1. These python scripts are used for testing the ETROC1 TDC chip
  - The **command\_interpret.py** file is a class for sockect communication
  - The **kc705\_mig\_control.py** file includes all kinds of functions such as I2C write/read, DDR3 data storage, Ethernet communication.

## 2. Hardware platform
  - The FPGA is Xilinx KC705 EVB and the FPGA socket address is 192.168.2.x, The x is configurable via switch (DIP switch SW11 positions 1 and 2 control the value of `x`, the positions 1 and 2 are **ON**, `x=3`, the position 1 is **ON** and the position 2 is **OFF**, `x=1`, and so forth) and its value ranges from 0 to 3 and the port number is fixed to 1024. [Schematic of KC705 EVB](https://www.xilinx.com/support/documentation/boards_and_kits/kc705_Schematic_xtp132_rev1_1.pdf)
  ```verilog
	hostname = '192.168.2.3'			#FPGA IP address
	port = 1024					#port number
  ```
  - KC750 EVB Picture is shown as below:
  ![KC705 EVB Picture](https://github.com/weizhangccnu/Python_Script/blob/master/ETROC1_TDC_Test_Software/Img/KC705_EVB.png)
  - The python scripts can be executed both on Windows and Linux operating system.
  - The Ethernet cable is connected between the PC and KC705 EVB.  
  - I2C interface mapping is shown as below figure.
  ![I2C interface Mapping](https://github.com/weizhangccnu/Python_Script/blob/master/ETROC1_TDC_Test_Software/Img/I2C_Interface_Mapping.png)
  - Ethernet communication speed is 1Gbps. Please make sure that the Ethernet cable can meet the requirements.

## 3. Software version
  - Firmware was synthesized and implemented on Vivado 2016.2
  - Python version: **python3.7.5** and the python scripts are all executed on **Atom IDE** with terminal package. You can choose other IDE as python interpreter according to your habits.
  - Before you execute the above python scripts, you should make sure that all the modules imported at the begin of each python file have already been installed. Otherwise, you must install all used modules with the command of `pip install modulename`

## 4. FPGA GTX reference clock configuration
  - The GTX reference clock is generated by Si5338 clock generator and its frequency is **160 MHz**. The GTX is not sensitive to the ploarity of reference clock.
  - The Si5338 EVB is configured by ClockBuilder Pro v.2.37.0.1 [ClockBuilder Pro download link](https://www.silabs.com/products/development-tools/software/clockbuilder-pro-software)
  - [Si5338-EVB User's Guide](https://www.silabs.com/documents/public/user-guides/Si5338-EVB.pdf)

## 5. Test Procedures
**1.** Download `kc705_mig.bit` file into FPGA.
  - [kc705_mig.bit file link](https://github.com/weizhangccnu/FPGA_Project/tree/master/kc705_ETROC1_TDC_Test_20191030/kc705_mig.runs/impl_1)
  - FPGA configuration mode: DIP switch SW13 positions 3, 4, and 5 control whose configuration mode is used at power-up or when the PROG pushbutton is pressed. The SW13 should be set as shown the below figure.
  ![FPGA Configuration mode](https://github.com/weizhangccnu/Python_Script/blob/master/ETROC1_TDC_Test_Software/Img/FPGA_Configuration_mode.png)
  - Launch **open hardware manager** menu on Vivad IDE and download `kc705_mig.bit` file into FPGA.

**2.** Verify Ethernet communiction.
  - Open windows doc terminal and using `ping 192.168.2.3` command to verify the Ethernet connection is working or not. If the Ethernet connection is wroking, all sent package will be received, otherwise not.
  - If the Ethernet connection is well, The RX and TX identification LED near the Ethernet socket will blink when execute the command of `ping 192.168.2.3`.

**3.** Provide reference clock to GTX. 
  - Using a USB cable connects the PC with Si5338-EVB and Using Clockbuilder Pro configures Si5338-EVB to generat a 160 MHz differential output clock at CLK0A/CLK0B SMA connector.  
  - Between the Si5338-EVB and KC-705 EVB is connected by a piar of coxial cable. The **J15** and **J16** are the GTX reference clock input SMAs. Before connecting the reference clock, you should make sure that the clock frequency is 160 MHz.
  
**4.** Verify I2C write and read functions.
  - Firstly, we should connect ETROC1 TDC test board I2C interface to the FPGA according to the FPGA I2C interface mapping figure.
  - Using `iic_read(mode, slave_addr, wr, reg_addr)` function read the register default value of ETROC1 TDC I2C controller and compare the read out default value with the set default value.
  - Using `iic_write(mode, slave_addr, wr, reg_addr, data)` function write some register value and Using `iic_read(mode, slave_addr, wr, reg_addr)` function read back this register value at once. Compare write in register data with read out data from register. If the read out data is identical with the write in data, it demonstrate that the I2C write and read functions are correct. 

**5.** Verify DDR3 data fecthing function.
