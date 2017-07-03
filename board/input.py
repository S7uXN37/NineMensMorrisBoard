#!/usr/bin/env python
import RPi.GPIO as GPIO

# Hardware SPI
SPI_PORT = 0
MCP = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, 0))
CS = [1,2,3]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(CS_EXTRA, GPIO.OUT, initial=GPIO.HIGH)

# Reads one MCP chip, pass MCP3008 object and CS pin
def read_mcp(mcp, cs):
    values = [0]*8
    for i in range(8):
        # read_adc() will get the value of the specified channel (0-7).
        GPIO.output(cs, GPIO.LOW)
        values[i] = mcp.read_adc(i)
        GPIO.output(cs, GPIO.HIGH)
    return values


def readBoard():
    inner = read_mcp(MCP, CS[0])
    middle = read_mcp(MCP, CS[1])
    outer = read_mcp(MCP, CS[2])

def hookPressure():
    #text
