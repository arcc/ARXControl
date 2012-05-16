
class Channel(object):
    """Channel representation."""

    #: Maximum Attenuator Level
    MAX_ATTENUATOR_LEVEL = 15

    #: Attenuator step (in dB)
    ATTENUATOR_STEP = 2

    def __init__(self, ch_id):
        self.chan_id = ch_id
        #:Attenuator level (0-15) in 2db steps.
        self.atten0 = 0
        #:Attenuator level (0-15) in 2db steps.
        self.atten1 = 0
        #:Front End Power. Boolean
        self.power = True
        #:Filterbank (0-2) 
        self.filterbank = 0
    
    def __repr__(self):
        return "<%s ID:%s %s,%s,%s,%s>"%(self.__class__.__name__,self.chan_id,
                                         self.atten0,self.atten1,self.power,
                                         self.filterbank,)
