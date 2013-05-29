from . import const
from .err import CheckError, WriteError

def unpack(self, inputstring):
    """
    Unpacks an ACU Command Structure into a tuple.

    :param inputstring: ACU Command String (or Response String).

    :rtype: A tuple of (CMD Code | RESP Code, ARGS | RESP String | None). 
    """
    inputstring = inputstring.strip(const.END_COMMAND)
    parts = inputstring.split(const.SEPARATOR)

    command = int(parts[0])
    try:
        args = parts[1].split(const.ARG_SEPARATOR)
        for i in range(len(args)):
            try:
                args[i] = int(args[i])
            except ValueError:
                pass
    except IndexError:
        args = None

    return command, args

from .connection import Connection



class ARX(object):
    """
    ARX Control Object.

    :attr:`power`, :attr:`attenN` ,and :attr:`filter` are all implemented via
    Python properties. When their values are accessed, the underlying system
    fetches the current values from the ACU. When they are assigned values, the
    values are validated, then transmitted to the ACU, when also validates and
    then applies the new setting.
    """

    _unpack = unpack

    def __init__(self, tty, rate=None):
        """
        Creates a new instance of ARX.

        :param tty: `port` parameter for serial connection to ARX.
        """
        self.conn = self._connect(tty,rate)
        self.conn_failure = 0
        self.check_error = 0
        #self._setup()
        self._initialize()

    def _setup(self):
        """Setup hook."""
        #: List of booleans. Represents FEE Power
        self.power = [False for i in range(4)]
        #: Atten 0, 0-15
        self.atten0 = 15
        #: Atten 1, 0-15
        self.atten1 = 15
        #: Filter, 0-2
        self.filter = 0

    def _initialize(self):
        """Initialization hook."""
        #self.read()
        pass

    def _connect(self, tty, rate):
        """Connection hook. Useful for testing."""
        return Connection(tty,rate)

    def _send(self, *args):
        """
        Wraps :attr:`ARXControl.connection.Connection._make_cmd` with retrying
        to ease use of communication system.

        Takes same parameters as
        :attr:`ARXControl.connection.Connection._make_cmd`

        :rtype: String containing ACU Response Message.
        """
        error_cnt = 0
        with self.conn as conn:
            rsp=''
            while error_cnt < const.MAX_RETRIES:
                conn.write(self.conn._make_cmd(*args))
                code, resp = self._unpack(conn.read(const.BUFFER_SIZE))

                if code is not const.kACK:
                    error_cnt += 1
                    rsp = resp
                else:
                    return resp
            cmd_str = self.conn._make_cmd(*args)
            raise IOError("Could not execute `%s`. Recieved response `%s`"%(
                            cmd_str,rsp))

    @property
    def power(self):
        """
        Interface to the ACU FEE Power system. When assigned a single boolean
        value, it assigns that value to all FEE Channels. When assigned a
        four-element list, it assigns the ith element of the list to the ith
        channel. When accessed, it fetches the current state from the ACU.
        """
        out = []
        for i in range(4):
            resp = self._send(const.FEE_READ,i)
            out.append(int(resp[0]))
        return out

    @power.setter
    def power(self,pwr):
        if hasattr(pwr,'__iter__'):
            if len(pwr) == 4:
                for i in range(4):
                    try:
                        pwr[i] = int(pwr[i])
                    except ValueError:
                        raise ValueError(
                            "power can only accept 0/1 or boolean True/False")
                    if pwr[i] == 1 or pwr[i] == 0:
                        self._send(const.FEE_WRITE,i,pwr[i])
                    else:
                        raise ValueError(
                            "power can only accept 0/1 or boolean True/False")
            else:
                raise ValueError(
                    "power must be either a single value or a four "
                    "element iterable")
        else:
            try:
                pwr = int(pwr)
            except ValueError:
                raise ValueError(
                    "power must be either an int or a four element iterable")

            if pwr == 1 or pwr == 0:
                for i in range(4):
                    self._send(const.FEE_WRITE,i,pwr)
            else:
                raise ValueError(
                    "power can only accept 0/1 or boolean True/False")

    @property
    def filter(self):
        """
        Interface to the ACU Filter system. When assigned an int (0-2), it sets
        the ACU to the selected filter. When accessed, it fetches the current
        state from the ACU.
        """
        resp = int(self._send(const.FILTER_READ)[0])
        return resp
            
    @filter.setter
    def filter(self,value):
        if 0 <= value <= 2:
            if value == int(value):
                resp = self._send(const.FILTER_WRITE,value)
            else:
                raise ValueError("Filter does not accept float values")
        else:
            raise ValueError("Attempt to set filter out of range (0-2)")

    @property
    def atten0(self):
        """
        Interface to the ACU Attenuator system, attenuator 0. When assigned a
        level (0-15), it sets the ACU to the selected level. When accessed, it
        fetches the current state from the ACU.
        """
        resp = int(self._send(const.ATTEN_READ,0)[0])
        return resp

    @atten0.setter
    def atten0(self,level):
        if 0 <= level <= 15:
            if level == int(level):
                resp = self._send(const.ATTEN_WRITE,0,level)
            else:
                raise ValueError("Atten0 does not accept float values")
        else:
            raise ValueError("Attempt to set atten0 out of range (0-15)")

    @property
    def atten1(self):
        """
        Interface to the ACU Attenuator system, attenuator 1. When assigned a
        level (0-15), it sets the ACU to the selected level. When accessed, it
        fetches the current state from the ACU.
        """
        resp = int(self._send(const.ATTEN_READ,1)[0])
        return resp

    @atten1.setter
    def atten1(self,level):
        if 0 <= level <= 15:
            if level == int(level):
                resp = self._send(const.ATTEN_WRITE,1,level)
            else:
                raise ValueError("Atten1 does not accept float values")
        else:
            raise ValueError("Attempt to set atten1 out of range (0-15)")

    @property
    def eeprom_offset(self):
        """
        Interface to the ACU EPPROM storage system. It reports the position
        offset for the storage system. When accessed, it fetches the current
        state from the ACU.
        """
        resp = int(self._send(const.EEPROM_READ)[0])
        return resp

    @eeprom_offset.setter
    def eeprom_offset(self,position):
        if 0 <= position <= (const.EEPROM_SIZE/const.FLASH_SIZE):
            if position == int(position):
                resp = self._send(const.EEPROM_WRITE,position)
            else:
                raise ValueError("EEPROM_OFFSET does not accept float values")
        else:
            raise ValueError("Attempt to set EEPROM_OFFSET out of range (0-15)")

    def roach(self, state):
        if 0 <= state <= 1:
            resp = self._send(const.ROACH_WRITE, state)
            if resp[0] == const.ROACH_WRITTEN:
                return state
        else:
            raise ValueError("Attempt to set ROACH to state out of range (0-1)")


    def write_flash(self):
        resp = self._send(const.FLASH_WRITE)
        return True

    

