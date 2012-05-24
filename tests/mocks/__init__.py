#from mockserial import Serial as MockSerial

from bitstring import BitArray, Bits, BitStream

from ARXControl import ARX, const 
from ARXControl.connection import Connection

class MockConnection(Connection):
    """
    Mocked version of :class:`Connection`.

    Overwrites :meth:`_connect` to replace :class:`Serial` with
    :class:`MockACU`.
    """

    def _connect(self, tty):
        return MockACU(tty)


class MockARX(ARX):
    """
    Mocked version of :class:`ARX`.
    
    Overwrites :meth:`_connect` to replace with :class:`MockConnections`.
    Also overwrites :meth:`_initialize` to remove opening :meth:`read`.
    """

    def _connect(self, tty):
        return MockConnection(tty)

    def _initialize(self):
        pass


class MockACU(ARX):
    """
    Mock object to emulate the ARX Control Unit.

    Emulates a serial connection, and behaves like the ACU when
    given commands.
    """

    DEFAULT_STATE = Bits('0xfff01f10')
    """
    Simulated response from ARX Control Unit.

    Consists of:

    +------+----------+------------------------+
    | Byte | Segment  | Value                  |
    +======+==========+========================+
    | 1    | START    | 0xFF                   |
    +------+----------+------------------------+
    | 2    | Ch 1     | Lvl:15, Lvl:0          |
    +------+----------+------------------------+
    | 3    | FB & FEE | On, and On, On, On, On |
    +------+----------+------------------------+
    | 4    | Checksum | 0x10                   |
    +------+----------+------------------------+
        
    """

    FRAME_LEN = const.FRAME_SIZE*8

    def __init__(self, tty=None):
        self.responses = {4: self._ready,
                         5: self._read,
                         6: self._write}
        self._resp_buffer = ''
        self.state = self._unpack(BitStream(self.DEFAULT_STATE))
        self._setup()
        self._update()

    def _ready(self,msg=None):
       self._resp_buffer = const.kREADY.bytes

    def _write(self, msg=None):
        if msg is not None:
            self.state = self._unpack(BitStream(msg))
            self._resp_buffer = const.kACK.bytes
    
    def _read(self, msg=None):
        state = self.state['start'] + self.state['atten'] + self.state['fb'] +\
        self.state['fee'] + self.state['checksum']

        self._resp_buffer = state.bytes
    
    def read(self, numberOfBytes):
        return self._resp_buffer

    def write(self, inputstring):
        in_bitarray = BitArray(bytes=inputstring)
        # Strips ending ';'
        in_bitarray.replace(const.END_COMMAND,Bits())

        #command, msg = list(BitArray(bytes=inputstring).split(const.SEPARATOR))
        split = list(in_bitarray.split(const.SEPARATOR))
        if len(split) == 1:
            msg = None
            command = split[0]
        elif len(split) >= 2:
            command = split[0]
            msg = split[1]
            # Strips ','
            msg.replace(const.SEPARATOR,Bits())
         
        self.responses[command.uint](msg)
 
