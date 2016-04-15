#!/usr/bin/python
#
# Read or Write data from/to the Adafruit 32KB I2C FRAM Breakout Board  
# from Raspberry Pi 
#
# Can be called from command line or public functions can be imported:
#
#    string = FRAMread(int address, int length)
#       (to retrieve binary data, use ord() on characters in string)
#
#    FRAMwrite(int address, string data)
#       (to write binary data, concatenate into a string using chr())
#
# (c) David Pease, April, 2016
#

# import needed functions
from sys    import argv, exit
from ctypes import *
from fcntl  import ioctl

# Public function to write to FRAM
def FRAMwrite(address, string):

   __doFramIO(address, data=string)

# Public function to read from FRAM
def FRAMread(address, length):

   return __doFramIO(address, length=length)

# Private function to perform FRAM I/O using ioctl
def __doFramIO(addr, data="", length=0):

   FRAM_ADDR = 0x50             # default FRAM I2C address

   # constant values from /usr/include/linux/i2c-dev.h
   I2C_RDWR = 0x0707            # ioctl value for combined R/W transfer
   I2C_M_RD = 0x01              # ioctl command flag for read

   # i2c command description structure                 # from <linux/i2c-dev.h>
   class i2c_msg(Structure):
      _fields_ = [("addr",  c_ushort),
                  ("flags", c_ushort),
                  ("len",   c_ushort),
                  ("buf",   c_char_p) ]

   # array of i2c command descriptions
   class msgarray(Structure):
      _fields_ = [("msg0",  i2c_msg),
                  ("msg1",  i2c_msg)]

   # i2c command list descriptor (head of structures)  # from <linux/i2c-dev.h>
   class i2c_rdwr_ioctl_data(Structure):
      _fields_ = [("msgs",  c_void_p),
                  ("nmsgs", c_ulong)]

   # determine read/write mode, set number of ioctl commands needed
   if len(data) > 0:
      write = True
      cmdcnt = 1
   else:
      write = False
      cmdcnt = 2

   # validate FRAM address range
   if addr + len(data) + length > 32768:
      raise ValueError('I/O address out of range.')

   # create write string, compute read/write data lengths
   writestr = chr(addr >> 8) + chr(addr & 0x00ff) + data
   writelen = len(writestr)
   readlen  = length

   # create buffers and buffer pointers for ioctl commands
   rwaddr_data = create_string_buffer(writestr, writelen)
   p_rw_data = cast(pointer(rwaddr_data), c_char_p)
   if write:
      p_buffer  = cast(None, c_char_p)
   else:
      buffer = create_string_buffer(readlen)
      p_buffer = cast(pointer(buffer), c_char_p)

   # initialize array of command descriptors (second is unused for write)
   msgs = msgarray(
           (FRAM_ADDR,        0, writelen, p_rw_data),
           (FRAM_ADDR, I2C_M_RD,  readlen, p_buffer))

   # set command array pointer to descriptor list, specify command count
   cmds = i2c_rdwr_ioctl_data(cast(pointer(msgs),c_void_p), cmdcnt)

   # open the Raspberry Pi I2C bus for reading and writing
   fd = open("/dev/i2c-1", "rw")

   # issue ioctl to read or write FRAM
   rc = ioctl(fd, I2C_RDWR, cmds)
   if rc != cmdcnt:
      raise IOError('Not all ioctl commands processed successfully.')

   # close the bus (file descriptor)
   fd.close()

   # return read buffer for read, otherwise nothing
   if write:
      return 
   else:
      return buffer.raw

# if invoked from command line, perform function and print result
if __name__ == "__main__":

   # validate inputs (minimally)
   if len(argv) != 4:
      print "%s: Invalid number of arguments; should be 3." % argv[0]
      exit(12)
   if argv[1] not in ("-r", "-w"):
      print "%s: Invalid read/write option (-r/-w)." % argv[0]
      exit(12)

   # call read or write function as requested 
   address = int(argv[2]);
   if argv[1] == "-w":
      FRAMwrite(address, argv[3])
   else:
      data = FRAMread(address, int(argv[3]))
      print data
 
   # we got this far without an exception so return success 
   exit(0)

