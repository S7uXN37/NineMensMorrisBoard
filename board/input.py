#!/usr/bin/env python
import RPi.GPIO as GPIO

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
CS = [18,26,22]
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

lower_bound = 520
upper_bound = 540

GPIO.setmode(GPIO.BOARD)
for _cs in CS:
    GPIO.setup(_cs, GPIO.OUT, initial=GPIO.HIGH)

def read_mcp(cs):
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        GPIO.output(cs, GPIO.LOW)
        v = mcp.read_adc(i)
        if v < lower_bound:
            values[i] = -1
        elif v > upper_bound:
            values[i] = 1
        else:
            values[i] = 0
        GPIO.output(cs, GPIO.HIGH)
    return values


def readBoard():
    i = read_mcp(CS[0])  # inner
    m = read_mcp(CS[1])  # middle
    o = read_mcp(CS[2])  # outer
    # map from polar coordinates (ring, pos in ring) to 1D array for AI
    board = [o[3], o[2], o[1],   m[3], m[2], m[1],   i[3], i[2], i[1],
             o[4], m[4], i[4],   i[0], m[0], o[0],
             i[5], i[6], i[7],   m[5], m[6], m[7],   o[5], o[6], o[7]]
    return board

def shutdown():
    GPIO.output(CS, GPIO.HIGH)
