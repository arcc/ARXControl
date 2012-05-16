ARXControl
==========

ARXControl is the control module interface library for the `LoFASM ARX`_.

It provides a simple interface to the 4 Channel ARX system developed by
Joe Craig of UNM for the Center of Advanced Radio Astronomy's Low Frequency
All Sky Monitor.

It is not intended for direct interaction with the ARX, but is meant to be a
library used by a more complex LoFASM interface system.


Pinout
------

Pinout as mapped to an ATMega 2560 MCU.
The planned ARX Control Unit is a `JKDevices`_ `MegaMini ATMEGA2560`_ board.

.. include:: pinout.rst

Simple API
----------

.. module:: ARXControl

.. autoclass:: ARXControl.arx.ARX
    :members:

.. autoclass:: ARXControl.channel.Channel
    :members: 

.. _LoFASM ARX: http://cara.phys.utb.edu/LoFASM/ARX
.. _JKDevices: http://jkdevices.com
.. _MegaMini ATMEGA2560: http://jkdevices.com/arduino-megamini
