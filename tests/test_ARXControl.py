#import sys, os
#
#sys.path.insert(0, os.path.abspath('..'))

import unittest

from bitstring import BitStream, Bits

from .mocks import MockARX
from ARXControl import const

TEST_STATE_1 = Bits('0xfff01f10')
"""
Simulated response from ARX Control Unit.

Consists of:

+------+----------+------------------------+
| Byte | Segment  | Value                  |
+======+==========+========================+
| 1    | START    | 0xFF                   |
+------+----------+------------------------+
| 2    | Attens   | Lvl:15, Lvl:0          |
+------+----------+------------------------+
| 3    | FB & FEE | 1, and On, On, On, On  |
+------+----------+------------------------+
| 4    | Checksum | 0x10                   |
+------+----------+------------------------+
    
"""

TEST_STATE_2 = Bits('0xff0f0fff')
"""
Simulated response from ARX Control Unit.

Consists of:

+------+----------+------------------------+
| Byte | Segment  | Value                  |
+======+==========+========================+
| 1    | START    | 0xFF                   |
+------+----------+------------------------+
| 2    | Attens   | Lvl:0, Lvl:15          |
+------+----------+------------------------+
| 3    | FB & FEE | 0, and On, On, On, On  | 
+------+----------+------------------------+
| 4    | Checksum | 0xFF                   |
+------+----------+------------------------+
    
"""

FRAME_LENGTH = const.FRAME_SIZE*8
""":const:`~ARXControl.const.FRAME_SIZE` converted from bytes to bits"""


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
            conn.write(const.CHECK_READY.bytes)
            self.assertEqual(conn.read(1),const.kREADY.bytes)

    def test_checksum(self):
        self.assertEqual(self.arx._checksum(self.arx._unpack(
                            BitStream(TEST_STATE_1))).bytes,
                            TEST_STATE_1[-8:].bytes)

    def test_read(self):
        self.arx.conn.state = self.arx._unpack(BitStream(TEST_STATE_1))

        self.arx.read()

        with self.arx.conn as conn:
            conn.write(const.READ.bytes)
            resp = conn.read(8)
            self.assertEqual(resp,TEST_STATE_1.bytes)

        self.assertEqual(self.arx.state, 
                         self.arx._unpack(BitStream(bytes=resp)))

    def test_write(self):
        self.arx.state = self.arx._unpack(BitStream(TEST_STATE_2))
        self.arx._update()
        self.arx.write()

        with self.arx.conn as conn:
            conn.write(const.READ.bytes)
            resp = conn.read(8)

        self.assertEqual(self.arx.state, 
                         self.arx._unpack(BitStream(bytes=resp)))

        
