# tuppersat-pico-radio

Python library to interface with the TupperSat Telemetry Thingamabob.

This is a Raspberry Pi Pico-compatible port of the earlier `tuppersat-radio`
project.


* * * * * * * * * *

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


* * * * * * * * * *

## Communicating with your TupperSat using `tuppersat.radio`

`tuppersat.radio` provides a simple API to handle assembling, formatting and
transmitting telemetry and data packets in forms that comply with the
requirements of the TupperSat Telemetry and Data Relay System. This is
provided through the `TupperSatRadio` class.

### Initialisation

To create a `TupperSatRadio` object, you need to provide it with a UART
object, a 1-byte address, and an 8-character ASCII callsign. A basic example:

```python
# uPython imports
from machine import UART, Pin

# tuppersat imports
from tuppersat.radio import TupperSatRadio

# constants
ADDRESS = ...
CALLSIGN = ...
BAUDRATE = 38400

# create the UART interface
uart = UART(1, baudrate=BAUDRATE, tx=Pin(4), rx=Pin(5))

radio = TupperSatRadio(uart, address, callsign)
```

We will assign callsigns and addresses to each team. See
`examples/pico_simple_telemetry.py` for a full example.

Note: you should initialise the `TupperSatRadio` object once when the program
starts.

### Transmitting Messages

To send telemetry and data packets, you can call the `send_telemetry` and
`send_data` methods of the `TupperSatRadio` object.

#### Telemetry Packets

The TupperSat telemetry format is prefaced by a `T` specifier, and consists of
the following fields separated by `|`:

  | Field       | Meaning                      | Type              |
  |-------------|------------------------------|-------------------|
  | callsign    | 8 letter identifier          | N/A               |
  | index       | integer less than 99999      | N/A               |
  | hhmmss      | time                         | Time (see below)  |
  | latitude    | latitude (decimal degrees, +ve northern hemisphere) | float |
  | longitude   | longitude (decimal degrees, +ve eastern hemisphere) | float |
  | hdop        | horizontal dilution of precision      | float    |
  | altitude    | altitude (metres)            | float             |
  | t_internal  | internal temperature (deg C) | float             |
  | t_external  | external temperature (deg C) | float             |
  | pressure    | pressure in millibars        | float             |

Telemetry packets can be sent by `TupperSatRadio.send_telemetry`. The first
two fields are filled out automatically. The user must supply the remaining
fields. A sensible way to prepare these additional fields is as items in a
dictionary. They can then be passed to `send_telemetry` using:

```python
from tuppersat.radio.

telemetry_dict = {
    'hhmmss'      : Time(hour=12, minute=34, second=56),
    'lat_dec_deg' : 53.3498,
    'lon_dec_deg' : -6.2603,
    # etc.
    }

radio.send_telemetry(**telemetry_dict)
```

You must pass values for all of these fields to `send_telemetry`. If there are
any fields where the telemetry value is missing, you must pass `None` for that
field, and `TupperSatRadio` will know what to do.

##### `Time`

The time telemetry field (`'hhmmss'`) needs to provide the hexagisemal parts
of the time. Since MicroPython has no `datetime` module, and you have no
real-time clock, is easiest done using the timestamp given by the GPS data.

The following code snippet should handle this:

```python
from ucollections import namedtuple

Time = namedtuple('Time', 'hour minute second microsecond')

def chunk(string, n):
    """Break a string into chunks of length n."""
    return (string[i:i+n] for i in range(0, len(string), n))

def parse_time(time_str):
    """Parse a time string HHMMSS.SSS into a Time object."""

    # split out the second and sub-second times
    _hhmmss, _milliseconds = time_str.split('.')

    # compute the sub-second time in microseconds
    _us = int(_milliseconds) * 1000

    # compute the hours, minutes and seconds
    _hh, _mm, _ss = (int(x) for x in chunk(_hhmmss, 2))

    return Time(_hh, _mm, _ss, _us)
```

Example usage:
```
>>> parse_time('123456.789')
Time(hour=12, minute=34, second=56, microsecond=789000)
```

#### Data Packets

The TupperSat data format is prefaced by a 'D' specifier and consists
of the following fields separated by '|':

  | Field       | Meaning                      | Type              |
  |-------------|------------------------------|-------------------|
  | callsign    | 8 letter identifier          | N/A               |
  | data        | specified by user            | bytes-like        |

The `SatRadio.send_data` message is designed to handle the message formatting
and to transmit the data object. The callsign is automatically attached and
encoded for you.  The data must be provided as a bytes-like object. i.e., as
one of:
* a bytes object,
* a bytearray,
* an iterable of integers between 0 and 255.

A simple example looks like:

```python
# these are equivalent
data = b'Hello World'
data = bytearray(b'Hello World')
data = [104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100]

radio.send_data(data)
```

You are free to customise the contents of your data packet to suit your
mission goals, subject to the following restrictions:
* it shall be no more than 240 bytes long.

Be aware that the bytes with value `0x10` actually take up 2 bytes. If you are
transmitting binary data, this may matter to you. If you are transmitting pure
ASCII text, this will not be important.

You may also wish to consider the following advice:
* Think about what processing needs to be done in-flight and what can be done
  in post-flight analysis. It is sensible to send as much raw data as
  possible. It is usually easier to apply analysis afterwards, rather than to
  undo that analysis if you actually need the unprocessed data (eg, to debug
  any odd sensor behaviour in flight).
* The pipe character `|` is used to separate TupperSat telemetry and data
  fields. You should use a _different_ delimiter for your own fields within
  your data. eg., if you are working with ASCII text, you might use `':'`,
  `';'` or `','`.


### Receiving Messages

TBC

* * * * * * * * * *