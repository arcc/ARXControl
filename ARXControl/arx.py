from bitstring import BitArray, BitStream, Bits, ReadError as BS_ReadError

from .connection import Connection
from . import const
from .err import CheckError, WriteError


class ARX(object):
    """ARX Control Object."""

    def __init__(self, tty):
        """
        Creates a new instance of ARX.

        :param tty: `port` parameter for serial connection to ARX.
        """
        self.conn = self._connect(tty)
        self.conn_failure = 0
        self.check_error = 0
        self._setup()
        self._initialize()

    def _setup(self):
        """Setup hook."""
        #: List of booleans. Represents FEE Power
        self.power = [False for i in range(4)]
        #: Atten 0, 0-15
        self.atten0 = 0
        #: Atten 1, 0-15
        self.atten1 = 0
        #: Filter, 0-2
        self.filter = 0


    def _initialize(self):
        """Initialization hook."""
        self.read()

    def _connect(self, tty):
        """Connection hook. Useful for testing."""
        return Connection(tty)

    def _checksum(self, state):
        """
        Calculate checksum of unpacked message.

        :param state: Dictionary of BitArray objects created by
            :meth:`~ARXControl.ARX._unpack`
        :rtype: Bits
        """
        return state['start'] ^ state['atten'] ^ (state['fb'] + state['fee'])

    def _unpack(self, state_stream):
        """
        Unpacks serial stream from control unit.

        :param state_stream: BitStream instance containing state frame.
        :rtype: Dictionary of BitArrays.
        """
        state = {}
        state['start'] = state_stream.read(8)
        state['atten'] = state_stream.read(8)
        state['fb'] = state_stream.read(4)
        state['fee'] = state_stream.read(4)
        try:
            state['checksum'] = state_stream.read(8)
        except BS_ReadError:
            pass

        return state

    def _update(self):
        """
        Takes :attr:`~ARXControl.state` and updates :attr:`~ARXControl.channels`
        """
        fee = list(self.state['fee'].cut(1))
        
        for i in range(len(self.power)):
            self.power[i] = fee[i]
        self.filterbank = self.state['fb']
        self.atten0, self.atten1 = map(lambda x: x.uint,
                                       list(self.state['atten'].cut(4)))

    def read(self):
        """
        Reads current ARX configuration. Updates internal dictionary
        :attr:`~ARXControl.ARX.state`.
        """
        with self.conn as conn:
            while self.check_error < const.MAX_RETRIES:
                conn.write(const.READ.bytes)
                state_stream = BitStream(bytes=conn.read(const.FRAME_SIZE))

                state = self._unpack(state_stream)

                try:
                    if self._checksum(state) == state['checksum']:
                        self.check_error = 0
                        self.state = state
                        self._update()
                        return True
                    else:
                        self.check_error += 1
                except KeyError:
                    raise CheckError(
                            "Message from control unit cannot be verified.")

            raise CheckError("Message from control unit cannot be verified.")

    def _atten_translate(self, atten):
        """
        Converts an atten level to binary representation.

        :rtype: Bits 4 bits long.
        """
        return Bits(uint=atten, length=4)

    def _translate(self):
        """
        Converts internal states to message pack.

        :rtype: BitArray of length :attr:`~ARXControl.const.FRAME_SIZE`.
        """
        attens = BitArray()

        attens.append(self._atten_translate(self.atten0))
        attens.append(self._atten_translate(self.atten1))
        fb = Bits(uint=self.filter, length=4)
        fee = Bits(self.power)

        message = const.START_BYTE + attens + fb + fee
        checksum = self._checksum(self._unpack(BitStream(message)))

        return message + checksum

    def write(self):
        """
        Writes internal states to ARXControl
        """
        with self.conn as conn:
            comm_frame = const.WRITE + const.SEPARATOR + self._translate()+\
                    const.END_COMMAND 
            
            conn.write(comm_frame.bytes)
            if conn.read(1) == const.kACK.bytes: 
                return True
            else:
                raise WriteError("Did not recieve ACK on write attempt.") 
