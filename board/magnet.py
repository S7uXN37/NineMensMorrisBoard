#!/usr/bin/env python
import RPi.GPIO as GPIO

PIN_A = 20
PIN_B = 20

# Initialize to LOW
GPIO.setup(PIN_A, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_B, GPIO.OUT, initial=GPIO.LOW)

def turnOn(color):
    if color<0:
        GPIO.output(PIN_A, GPIO.HIGH)
        GPIO.output(PIN_B, GPIO.LOW)
    else:
        GPIO.output(PIN_A, GPIO.LOW)
        GPIO.output(PIN_B, GPIO.HIGH)

def turnOff():
    GPIO.output(PIN_A, GPIO.LOW)
    GPIO.output(PIN_B, GPIO.LOW)