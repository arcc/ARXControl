from serial import Serial

from . import const
from .err import ConnError

class Connection(object):
    """
    Connection class. Provides a wrapper around a serial connection
    that verifies the ARX Control Unit is ready to accept commands.
    """

    def __init__(self, tty):
        """
        :param tty: `port` parameter for serial connection to ARX
        """
        self.serial = self._connect(tty)
        self.conn_failure = 0

    def _connect(self, tty):
        """Connect hook. Useful for testing hooks"""
        return Serial(tty)

    def __enter__(self):
        while self.conn_failure < const.MAX_RETRIES:
            self.serial.write(const.CHECK_READY.bytes)

            if self.serial.read(1) == const.kREADY.bytes:
                break
            self.conn_failure += 1

        if self.conn_failure >= const.MAX_RETRIES:
            raise ConnError(
                "Failure attempting to communicate with control unit.")

        return self.serial 
            
    def __exit__(self, etype, value, tb):
        self.conn_failure = 0
