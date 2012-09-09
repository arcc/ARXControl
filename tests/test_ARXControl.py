#import sys, os
#
#sys.path.insert(0, os.path.abspath('..'))

import unittest2 as unittest

from .mocks import MockARX
from ARXControl import const

#: Simulated Test State for ARX Control Unit.
TEST_STATE_1 = {'FEE':[1,1,1,1],
                'ATTEN':[7,7],
                'Filter':0,
                'EEPROM':1}

#: Simulated Test State for ARX Control Unit.
TEST_STATE_2 = {'FEE':[1,0,1,0],
                'ATTEN':[15,7],
                'Filter':0,
                'EEPROM':1}

class TestARXControl(unittest.TestCase):
    """
    Testcase for ARX Control.
    """

    def setUp(self):
        """Set up mock ARX and default responses""" 
        self.arx = MockARX('/dev/usbtty0')

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.arx
        
    def test_ready(self):
        with self.arx.conn as conn:
            conn.write(conn._make_cmd(const.ACU_READY))
            cmd, _ = conn._unpack(conn.read(10))
            self.assertEqual(str(cmd),str(const.kREADY))

    #def test_checksum(self):
        #self.assertEqual(self.arx._checksum(self.arx._unpack(
                            #BitStream(TEST_STATE_1))),
                            #TEST_STATE_1[-8:])

    def test_fee_default_states(self):
        defaults = self.arx.conn.serial.DEFAULT_STATE
        with self.arx.conn as conn:
            for i in range(4):
                conn.write(conn._make_cmd(const.FEE_READ,i))
                code,resp = conn._unpack(conn.read(10))
                self.assertEqual(int(code),const.kACK)
                self.assertNotEqual(resp,None)
                self.assertEqual(int(resp[0]),defaults['FEE'][i])

    def test_atten_default_states(self):
        defaults = self.arx.conn.serial.DEFAULT_STATE
        with self.arx.conn as conn:
            for i in range(2):
                conn.write(conn._make_cmd(const.ATTEN_READ,i))
                code,resp = conn._unpack(conn.read(10))
                self.assertEqual(int(code),const.kACK)
                self.assertNotEqual(resp,None)
                self.assertEqual(int(resp[0]),defaults['ATTEN'][i])

    def test_filter_default_states(self):
        defaults = self.arx.conn.serial.DEFAULT_STATE
        with self.arx.conn as conn:
            conn.write(conn._make_cmd(const.FILTER_READ))
            code,resp = conn._unpack(conn.read(10))
            self.assertEqual(int(code),const.kACK)
            self.assertNotEqual(resp,None)
            self.assertEqual(int(resp[0]),defaults['FILTER'])

    def test_eeprom_default_states(self):
        defaults = self.arx.conn.serial.DEFAULT_STATE
        with self.arx.conn as conn:
            conn.write(conn._make_cmd(const.EEPROM_READ))
            code,resp = conn._unpack(conn.read(10))
            self.assertEqual(int(code),const.kACK)
            self.assertNotEqual(resp,None)
            self.assertEqual(int(resp[0]),defaults['EEPROM'])


    def test_fee_all_write(self):
        # Testing Int assignment
        self.arx.power = 1 
        self.assertEqual(self.arx.power, [1,1,1,1])
        self.arx.power = 0 
        self.assertEqual(self.arx.power, [0,0,0,0])
        with self.assertRaises(ValueError):
            self.arx.power = 'A'

        # Testing Bool assignment
        self.arx.power = True 
        self.assertEqual(self.arx.power, [1,1,1,1])
        self.arx.power = False 
        self.assertEqual(self.arx.power, [0,0,0,0])
        with self.assertRaises(ValueError):
            self.arx.power = 'Foo'

    def test_fee_list_write(self):
        # Testing Int List assignment
        self.arx.power = [1,0,1,0]
        self.assertEqual(self.arx.power, [1,0,1,0])
        self.arx.power = [0,1,0,1]
        self.assertEqual(self.arx.power, [0,1,0,1])
        with self.assertRaises(ValueError):
            self.arx.power = [1,1]

        # Testing Bool List assignment
        self.arx.power = [True,True,True,True]
        self.assertEqual(self.arx.power, [1,1,1,1])
        self.arx.power = [False,False,False,False]
        self.assertEqual(self.arx.power, [0,0,0,0])
        with self.assertRaises(ValueError):
            self.arx.power = [False, False]

    def test_filter_write(self):
        for i in range(3):
            self.arx.filter = i
            self.assertEqual(self.arx.filter, i, "Setting filter to %s"%i)
        for x in ['A',5.12,30]:
            with self.assertRaises(ValueError, msg="Setting filter to %s"%x):
                self.arx.filter = x 

    def test_atten0_write(self):
        for i in range(16):
            self.arx.atten0 = i
            self.assertEqual(self.arx.atten0, i, "Setting atten0 to %s"%i)
        for x in ['A',5.12,30]:
            with self.assertRaises(ValueError, msg="Setting atten0 to %s"%x):
                self.arx.atten0 = x 

    def test_atten1_write(self):
        for i in range(16):
            self.arx.atten1 = i
            self.assertEqual(self.arx.atten1, i, "Setting atten1 to %s"%i)
        for x in ['A',5.12,30]:
            with self.assertRaises(ValueError, msg="Setting atten1 to %s"%x):
                self.arx.atten1 = x 

