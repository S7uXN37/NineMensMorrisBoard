#!/usr/bin/env python
import RPi.GPIO as GPIO

pinA = 13
pinB = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup([pinA, pinB], GPIO.OUT, initial=GPIO.LOW)

def turnOn(color):
    if color<0:  # TODO check
        GPIO.output(pinA, GPIO.HIGH)
        GPIO.output(pinB, GPIO.LOW)
    else:
        GPIO.output(pinA, GPIO.LOW)
        GPIO.output(pinB, GPIO.HIGH)

def turnOff():
    GPIO.output(pinA, GPIO.LOW)
    GPIO.output(pinB, GPIO.LOW)