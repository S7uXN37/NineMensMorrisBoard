# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
CS = [18,26,22]
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

GPIO.setmode(GPIO.BOARD)
for _cs in CS:
    GPIO.setup(_cs, GPIO.OUT, initial=GPIO.HIGH)

def read_mcp(cs):
    mcp_values = [0]*8
    for k in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        GPIO.output(cs, GPIO.LOW)
        mcp_values[k] = mcp.read_adc(k)
        GPIO.output(cs, GPIO.HIGH)
    return mcp_values


print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)
# Main program loop.
try:
    # Executing calibration for 10s
    minVal = 1024
    maxVal = 0
    try:
        print("Calibrating... You can interrupt with Ctrl+C")
        while True:
            for j in range(3):
                # Read all the ADC channel values in a list.
                values = read_mcp(CS[j])
                for x in values:
                    maxVal = max(maxVal, x)
                    minVal = min(minVal, x)
                # Print the ADC values.
                print(str(j) + ': | {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
    except KeyboardInterrupt:
        print("Interrupted.")    

    # Ask for lower and upper bounds
    lower_bound = int(raw_input("Lower bound (min="+str(minVal)+"): "))
    upper_bound = int(raw_input("Upper bound (max="+str(maxVal)+"): "))
    
    while True:
        for j in range(3):
            # Read all the ADC channel values in a list.
            values = read_mcp(CS[j])
            for i in range(8):
                if values[i] < lower_bound:
                    values[i] = -1
                elif values[i] > upper_bound:
                    values[i] = 1
                else:
                    values[i] = 0
            # Print the ADC values.
            print(str(j) + ': | {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
        print('  ')
        # Pause for half a second.
        time.sleep(0.5)

finally:
    GPIO.output(CS, GPIO.HIGH)
    GPIO.cleanup()
