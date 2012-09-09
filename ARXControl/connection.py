from serial import Serial

from .arx import unpack 
from . import const
from .err import ConnError

#def unpack(inputstring):
    #"""
    #Unpacks an ACU Command Structure into a tuple.

    #:param inputstring: ACU Command String (or Response String).

    #:rtype: A tuple of (CMD Code | RESP Code, ARGS | RESP String | None). 
    #"""
    #inputstring = inputstring.strip(const.END_COMMAND)
    #parts = inputstring.split(const.SEPARATOR)

    #command = parts[0]
    #try:
        #args = parts[1].split(const.ARG_SEPARATOR)
    #except IndexError:
        #args = None

    #print "Unpacked: ", command, "--", args
    #return command, args


class Connection(object):
    """
    Connection class. Provides a wrapper around a serial connection
    that verifies the ARX Control Unit is ready to accept commands.
    """
    _unpack = unpack

    def __init__(self, tty):
        """
        :param tty: `port` parameter for serial connection to ARX
        """
        self.serial = self._connect(tty)
        self.conn_failure = 0

    def _connect(self, tty):
        """Connect hook. Useful for testing hooks"""
        return Serial(tty, timeout=const.TIMEOUT, baudrate=const.BAUDRATE)

    def _split(self, resp):
        return resp.strip(';').split(',')

    def _make_cmd(self, cmd, *args):
        """
        Generates a command string

        :param cmd: Command Code, usually from :module:`.const`.
        :param args: One or two arguments used to build the command string.

        :rtype: A properly formatted string that meets the ACU Command
        Structure.
        """
        out = str(cmd)
        if args:
            if len(args) > 2:
                raise TypeError('Only accepts a maximum of two arguments')
            out += const.SEPARATOR+const.ARG_SEPARATOR.join(map(str,args))
        out += const.END_COMMAND
        return out 



    def __enter__(self):
        while self.conn_failure < const.MAX_RETRIES:
            self.serial.write(self._make_cmd(const.ACU_READY))

            cmd, _ = self._unpack(self.serial.read(const.FRAME_OFFSET))

            if  int(cmd) == const.kREADY:
                break
            self.conn_failure += 1

        if self.conn_failure >= const.MAX_RETRIES:
            raise ConnError(
                "Failure attempting to communicate with control unit.")

        return self.serial 
            
    def __exit__(self, etype, value, tb):
        self.conn_failure = 0
