#!/usr/bin/env python
import RPi.GPIO as GPIO
import serial

for i in range(10):
    try:
        port = '/dev/ttyACM%i' % i
        s = serial.Serial(port, 9600)
        print("Connected to Arduino on port: %s" % port)
        break
    except serial.serialutil.SerialException:
        print("Arduino not on port: %s" % port)
    if i == 9:
        raise RuntimeError("Could not find Arduino")

def turnOn(color):
    color = -color
    s.write(bytes('%i' % color, 'UTF-8'))
    resp = s.readline()
    print("Arduino: %s" % resp)

def turnOff():
    turnOn(0)

def shutdown():
    turnOff()
    s.close()
