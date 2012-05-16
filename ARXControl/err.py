
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class CheckError(Error):
    """
    Exception raised when reading from ARX Control Module Fails.
    """
    def __init__(self,msg=''):
        """
        :param msg: Error message.
        """
        self.msg = msg

    def __str__(self):
        return "'%s'"%self.msg

class ConnError(Error):
    """
    Exception raised when checksum verification fails.
    """
    def __init__(self,msg=''):
        """
        :param msg: Error message.
        """
        self.msg = msg

    def __str__(self):
        return "'%s'"%self.msg

class WriteError(Error):
    """
    Exception raised when write fails.
    """
    def __init__(self,msg=''):
        """
        :param msg: Error message.
        """
        self.msg = msg

    def __str__(self):
        return "'%s'"%self.msg


