#About this Module

##A Simple Python module for reading and writing to the Adafruit I2C FRAM breakout board using Python

###Background

The Adafruit I2C FRAM breakout board is a 32K non-volatile memory board using ferromagnetic RAM (FRAM).  FRAM has several 
properties that make it attractive for Maker projects needing non-volatile memory, including byte addressability (without
the need for a Flash Translation Layer (FTL)), and amazing write endurance (~10**12 overwrites per cell).  The board is
connected to a computer system using the I2C bus.  This makes it potentially usable by many types of small computers, 
including Arduinos and Raspberry Pis.  The Adafuit example code is for Adruino systems.

Connecting the board to a Raspberry Pi is trivial, and requires only 4 wries to get working: Vcc (5V or 3.3V), ground, SDA 
and SCL.  However, that is where the Raspberry Pi ease-of-use ends for this board.  The Python I2C (SMBus) module and the 
underlying Linux (Raspbian, etc.) i2c-dev library expect an I2C chip to use a 1-byte command id or register address in the I2C
command.  However, since the FRAM board is a 32K memory, it requires two address bytes.  Thus, the Python I2C module, and
even the standard i2c-dev Linux module cannot be used with the board.

###Implementation and Use

This module's pure Python code uses the fcntl module's ioctl() function along with the ctypes module's ability to build c-
language compatible data structures to implement read and write functions for the board from Python.  The program has a very 
simple interface, implementing multi-byte string reads and writes to arbitrary addresses. Of course, it can be used to read 
and write binary data, using the Python chr() function to encode binary numbers into characters, and the ord() function to 
convert the characters back to numeric values.

The module can be used as-is by doing the following:

1.  Put a copy of the FRAM.py program into the directory with the program that will use it.

2.  Include the module:
  - from FRAM import FRAMread, FRAMwrite

3.  Use the FRAMread and FRAMwrite functions to read and write the memory:
  - FRAMwrite(memoryaddress, string)
  - data = FRAMread(memoryaddress, length)

The default chip address of 0x50 is hardcoded at the top of the program, and can be trivially changed.

##Potential Enhancements

This module implements a very basic interface, and is largely intended as an example of how to access the FRAM from
Python on a Raspberry Pi.  It is useful as-is, but a much more sophisticated interface could be built using the same
basic code.  It's major shortcomging (in the author's opinion) include the fact that it has a hard-coded I2C bus 
address, only reads and writes strings, and opens and closes the i2c bus device for each call.  (However, this was
sufficient for the author's needs, and has already taken siginificant time to research and implement.)

A module that creates an FRAM object which is passed the FRAM I2C bus address at initialization and opens the bus
device only once would be a simple extenstion.  From there, a selection of read and write calls, such as write8(),
write16() and writeString(), along with the complementary read functions would be easy and would make the module very 
flexible.  (Folks who are familiar with the Adafruit Arduino driver will recognize that this is the same model as,
and an extension of, that driver.)

If anyone undertakes this implementation based on my code, I would enjoy hearing abou it.



