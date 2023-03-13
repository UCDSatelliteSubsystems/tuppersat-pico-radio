"""pico_simple_telemetry.py

A test script sending empty telemetry packets.

To see this in action, you will need to set up a second Telemetry Thingamabob
running a script like pico_simple_rx.py from the `tuppersat.rhserial` package.

"""

# standard library imports
from time import sleep

# uPython imports
from machine import UART, Pin

# tuppersat imports
from tuppersat.radio import TupperSatRadio

# constants
UART_ID = 1
TX_PIN = 4
RX_PIN = 5
T3_BAUDRATE = 38400

ADDRESS = 0xfe
CALLSIGN = 'TESTSAT1'

def loop(radio, pause=1):
    # send a blank telemetry packet.
    print('Sending telemetry')
    radio.send_telemetry(
        hhmmss     = None,
        latitude   = None,
        longitude  = None,
        hdop       = None,
        altitude   = None,
        t_internal = None,
        t_external = None,
        pressure   = None,
    )
    sleep(pause)

    
def main():
    # initialisation
    uart = UART(UART_ID, baudrate=T3_BAUDRATE, tx=Pin(TX_PIN), rx=Pin(RX_PIN))
    radio = TupperSatRadio(uart, ADDRESS, CALLSIGN)

    # main loop
    while True:
        loop(radio)

    

if __name__=="__main__":
    main()


