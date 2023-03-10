"""



"""

# standarad library imports
from time import sleep

# uPython imports
from machine import UART, Pin

# tuppersat imports
from tuppersat.radio import TupperSatRadiod

# constants
UART_ID = 1
TX_PIN = 4
RX_PIN = 5

T3_BAUDRATE = 38400

def loop(radio, pause=1):
    print('Sending telemetry')
    radio.send_telemetry()
    sleep(pause)

    
def main():
    # initialisation
    uart = UART(UART_ID, baudrate=T3_BAUDRATE, tx=Pin(TX_PIN), rx=Pin(RX_PIN))
    radio = TupperSatRadio(uart, callsign)

    # main loop
    while True:
        loop(radio)

    

if __name__=="__main__":
    main()


