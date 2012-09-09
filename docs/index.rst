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

Pinout as mapped to an ATMega328 (Arduino compatible for now).
Prototyping is based off of a standard Arduino Uno, but plans are to move to a
`USB Boarduino`_ by `Adafruit`_.

.. include:: pinout.rst

Simple API
----------

.. module:: ARXControl

.. autoclass:: ARXControl.arx.ARX
    :members:

.. _LoFASM ARX: http://cara.phys.utb.edu/LoFASM/ARX
.. _USB Boarduino: http://www.adafruit.com/products/91
.. _Adafruit: http://www.adafruit.com

Further Documentation
---------------------

For more info, continue below.

.. toctree::
    :maxdepth: 1

    api
    pinout
