# Comm constants
kCOMM_ERR = 0
kACK = 1
kREADY = 2
kERR = 3

# Commands
ACU_READY = 4
FEE_READ = 5
FEE_WRITE = 6
FILTER_READ = 7
FILTER_WRITE = 8
ATTEN_READ = 9
ATTEN_WRITE = 10
EEPROM_READ = 11
EEPROM_WRITE = 12
FLASH_WRITE = 13
ROACH_WRITE = 14

# Consts
MAX_RETRIES = 3
FRAME_SIZE = 4  # Bytes
FRAME_OFFSET = 15 # Bytes
BUFFER_SIZE = 100 # Bytes

SEPARATOR = ','
ARG_SEPARATOR = '|'
END_COMMAND = ';'

BAUDRATE = 57600 # Baudrate for Arduino Duemilanove (FTDI Comms)
#BAUDRATE = 115200 # Baudrate for Arduino Uno + (AT8u2 Comms)

TIMEOUT = 1 # Seconds

# Responses
READY_RSP = "READY"
FEE_WRITTEN = "FEE State Written"
FEE_RANGE = "FEE selection is out of range"
FILTER_WRITTEN = "Filter State Written"
FILTER_RANGE = "Filter selection is out of range"
ATTEN_WRITTEN = "Atten State Written"
ATTEN_RANGE = "Atten selection is out of range"
EEPROM_WRITTEN = "EEPROM Address Updated"
EEPROM_RANGE = "EEPROM Address is out of range"
FLASH_WRITTEN = "EEPROM Written"
ROACH_WRITTEN = "Roach Power State Written"
ROACH_RANGE = "Roach Power State is not out of range"

DATA_PARSE_FAIL = "Data string could not be parsed"

