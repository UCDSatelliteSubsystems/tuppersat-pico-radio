# tuppersat-pico-radio

Python library to interface with the TupperSat Telemetry Thingamabob.

This is a Raspberry Pi Pico-compatible port of the earlier `tuppersat-radio`
project.


## Getting Started

### Using MicroPython & Raspberry Pi Pico

#### Installation

If you are using MicroPython and the Pi Pico, you will need to place the
`tuppersat.radio` package somewhere that your program's import statements can
find it. If you have not already done so, you will also need to install the
`tuppersat.rhserial` package.

The suggested approach here is:

* clone this repository onto your working machine.

* clone the `tuppersat-rhserial` repository onto your working machine.

* create nested directories `tuppersat/`, `tuppersat/radio/`, and
  `tuppersat/rhserial/` in your Pico's root directory.

* use the Thonny IDE to copy the source code files into these directories.

* you will need to make the `tuppersat/` directory into a package. To do this,
  place a blank text file called `__init__.py` in the `tuppersat/` directory.


#### First Scripts

The `examples/pico_simple_telemetry.py` script transmits dummy telemetry
packets. Run this script on your Pi Pico, while running a script with receiver
functionalities on another laptop or Raspberry Pi.

### Using CPython & pip.

TBC


## Communicating with `tuppersat.radio`

TBC

* * * * * * * * * *