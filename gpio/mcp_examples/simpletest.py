# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO

# Software SPI configuration:
#CLK = 26
#D_OUT = 19
#D_IN = 13
#CS = 6
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=D_OUT, mosi=D_IN)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
CS = 38
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

GPIO.setmode(GPIO.BOARD)
GPIO.setup(CS, GPIO.OUT, initial=GPIO.HIGH)

print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)
# Main program loop.
try:
    while True:
        # Read all the ADC channel values in a list.
        values = [0]*8
        for i in range(8):
            # The read_adc function will get the value of the specified channel (0-7).
            GPIO.output(CS, GPIO.LOW)
            values[i] = mcp.read_adc(i)
            GPIO.output(CS, GPIO.HIGH)
        # Print the ADC values.
        print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
        # Pause for half a second.
        time.sleep(0.5)
finally:
    GPIO.cleanup()
