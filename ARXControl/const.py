
from bitstring import Bits

# Comm constants
kCOMM_ERR = Bits(uint=0,length=8)
kACK = Bits(uint=1,length=8)
kREADY = Bits(uint=2,length=8)
kERR = Bits(uint=3,length=8)
CHECK_READY = Bits(uint=4,length=8)
READ = Bits(uint=5,length=8)
WRITE = Bits(uint=6,length=8)
START_BYTE = Bits(uint=255,length=8)

# Consts
MAX_RETRIES = 3
FRAME_SIZE = 4  # Bytes
FRAME_OFFSET = 15 # Bytes
BUFFER_SIZE = 100 # Bytes

SEPARATOR = Bits(bytes=',')
END_COMMAND = Bits(bytes=';')

#BAUDRATE = 57600 # Baudrate for Arduino Duemilanove (FTDI Comms)
BAUDRATE = 115200 # Baudrate for Arduino Uno + (AT8u2 Comms)

TIMEOUT = 1 # Seconds
