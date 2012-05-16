from bitstring import BitArray, BitStream, Bits, ReadError as BS_ReadError

from .channel import Channel
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
        #: List of :class:`~ARXControl.channel.Channel` objects.
        self.channels = [Channel(i) for i in range(4)]
        self._initialize()

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
        return state['start'] ^ state['ch0'] ^ state['ch1'] ^ state['ch2'] ^ \
                state['ch3'] ^ state['fb'] ^ state['fee']

    def _unpack(self, state_stream):
        """
        Unpacks serial stream from control unit.

        :param state_stream: BitStream instance containing state frame.
        :rtype: Dictionary of BitArrays.
        """
        state = {}
        state['start'] = state_stream.read(8)
        state['ch0'] = state_stream.read(8)
        state['ch1'] = state_stream.read(8)
        state['ch2'] = state_stream.read(8)
        state['ch3'] = state_stream.read(8)
        state['fb'] = state_stream.read(8)
        state['fee'] = state_stream.read(8)
        try:
            state['checksum'] = state_stream.read(8)
        except BS_ReadError:
            pass

        return state

    def _update(self):
        """
        Takes :attr:`~ARXControl.state` and updates :attr:`~ARXControl.channels`
        """
        fb = list(self.state['fb'].cut(2))
        fee = list(self.state['fee'].cut(2))
        for i in range(len(self.channels)):
            ch = list(self.state['ch%s'%(i)].cut(4))
            self.channels[i].atten0 = ch[0].uint
            self.channels[i].atten1 = ch[1].uint
            self.channels[i].filterbank = fb[i].uint
            self.channels[i].power = fb[i][0]


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
        fee = BitArray()
        fb = BitArray()

        for channel in self.channels:
            attens.append(self._atten_translate(channel.atten0))
            attens.append(self._atten_translate(channel.atten1))
            fb.append(Bits(uint=channel.filterbank, length=2))
            fee.append(Bits(bool=channel.power))
            fee.append(Bits(bool=False))

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
