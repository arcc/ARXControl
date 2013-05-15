#from mockserial import Serial as MockSerial

from ARXControl import ARX, const 
from ARXControl.arx import unpack
from ARXControl.connection import Connection

class MockConnection(Connection):
    """
    Mocked version of :class:`Connection`.

    Overwrites :meth:`_connect` to replace :class:`Serial` with
    :class:`MockACU`.
    """

    def _connect(self, tty, rate):
        return MockACU(tty, rate)


class MockARX(ARX):
    """
    Mocked version of :class:`ARX`.
    
    Overwrites :meth:`_connect` to replace with :class:`MockConnections`.
    Also overwrites :meth:`_initialize` to remove opening :meth:`read`.
    """

    def _connect(self, tty, rate):
        return MockConnection(tty, rate)

    def _initialize(self):
        pass


class MockACU(ARX, Connection):
    """
    Mock object to emulate the ARX Control Unit.

    Emulates a serial connection, and behaves like the ACU when
    given commands.
    """

    

    DEFAULT_STATE = {'FEE':[0,0,0,0],
                     'ATTEN':[15,15],
                     'FILTER':0,
                     'EEPROM':1}


    def __init__(self, tty=None, rate=None):
        self.responses = {const.ACU_READY: self._ready,
                          const.FEE_READ: self._fee_read,
                          const.FEE_WRITE: self._fee_write,
                          const.FILTER_READ: self._filter_read,
                          const.FILTER_WRITE: self._filter_write,
                          const.ATTEN_READ: self._atten_read,
                          const.ATTEN_WRITE: self._atten_write,
                          const.EEPROM_READ: self._eeprom_read,
                          const.EEPROM_WRITE: self._eeprom_write}

        self._resp_buffer = ''
        self.state = self.DEFAULT_STATE

    def _build_resp(self,code=1,resp_str=None):
        out = str(code)
        if resp_str or resp_str is 0:
            out += const.SEPARATOR + str(resp_str)
        out += const.END_COMMAND
        return out


    #def _send_cmd(self, command, *args):
        #out = str(command)
        #if args or args is 0:
            #if len(args) > 2:
                #raise TypeError('Only accepts a maximum of two arguments')
            #out += const.SEPARATOR +  '|'.join(map(str,args))
        #out += const.END_COMMAND
        #return out 
        

    def _ready(self,msg=None):
        self._resp_buffer = self._build_resp(const.kREADY,const.READY_RSP)


    def _fee_read(self, args):
        if args[0] >=0 and args[0] < 4:
            state = self.state['FEE'][args[0]]
            self._resp_buffer = self._build_resp(const.kACK,
                                             state)
        else:
            self._resp_buffer = self._build_resp(const.kERR, const.FEE_RANGE)

   
    def _fee_write(self, args):
        if args is not None:
            if args[0] >=0 and args[0] < 4:
                self.state['FEE'][args[0]] = args[1]
                self._resp_buffer = self._build_resp(const.kACK,
                                        const.FEE_WRITTEN)
            else:
                self._resp_buffer = self._build_resp(const.kERR,
                                        const.FEE_RANGE)
        else:
            self._resp_buffer = self._build_resp(const.kERR,
                                    const.DATA_PARSE_FAIL)


    def _filter_read(self, args):
        self._resp_buffer = self._build_resp(const.kACK, self.state['FILTER'])
   
    def _filter_write(self, args):
        if args[0] >=0 and args[0] < 4:
            self.state['FILTER'] = args[0]
            self._resp_buffer = self._build_resp(const.kACK,
                                                 const.FILTER_WRITTEN)
        else:
            self._resp_buffer = self._build_resp(const.kERR, const.FILTER_RANGE)


    def _atten_read(self, args):
        if args is not None:
            if args[0] >=0 and args[0] < 2:
                self._resp_buffer = self._build_resp(const.kACK,
                                         self.state['ATTEN'][args[0]])
            else:
                self._resp_buffer = self._build_resp(const.kERR,
                                        const.DATA_PARSE_FAIL)
        else:
            self._resp_buffer = self._build_resp(const.kERR,
                                    const.DATA_PARSE_FAIL)
   
    def _atten_write(self, args):
        if args is not None:
            if args[0] >=0 and args[0] < 2:
                self.state['ATTEN'][args[0]] = args[1]
                self._resp_buffer = self._build_resp(const.kACK,
                                        const.ATTEN_WRITTEN)
            else:
                self._resp_buffer = self._build_resp(const.kERR,
                                        const.DATA_PARSE_FAIL)
        else:
            self._resp_buffer = self._build_resp(const.kERR,
                                    const.DATA_PARSE_FAIL)


    def _eeprom_read(self, args):
        self._resp_buffer = self._build_resp(const.kACK, self.state['EEPROM'])
   
    def _eeprom_write(self, args):
        if args is not None:
            if args[0] < 1024 and args[0] >=1:
                self.state['EEPROM'] = args[0]
                self._resp_buffer = self._build_resp(const.kACK,
                                                     const.EEPROM_WRITTEN)
            else:
                self._resp_buffer = self._build_resp(const.kERR,
                                        const.EEPROM_RANGE)
        else:
            self._resp_buffer = self._build_resp(const.kERR,
                                    const.DATA_PARSE_FAIL)

    #def _unpack(self, inputstring):
        #inputstring = inputstring.strip(const.END_COMMAND)
        #parts = inputstring.split(const.SEPARATOR)

        #command = parts[0]
        #try:
            #args = parts[1].split(const.ARG_SEPARATOR)
            #for i in range(len(args)):
                #try:
                    #args[i] = int(args[i])
                #except ValueError:
                    #pass
        #except IndexError:
            #args = None

        #return command, args
        

    def read(self, numberOfBytes):
        """
        Emulates Serial interface. 

        Takes the same arguments as :func:Serial.read but does not respect the
        `numberOfBytes` argument. 

        Returns the response generated by the last :func:write command.
        """
        return self._resp_buffer

    def write(self, inputstring):
        """
        Emulates Serial interface. 

        Takes the same arguments as :func:Serial.write.

        Sets up a response generated by the issued command, which can be
        retrieved via the :func:read command.
        """
        command, args = self._unpack(inputstring)
        if int(command) < max(self.responses):
            self.responses[int(command)](args)
 
