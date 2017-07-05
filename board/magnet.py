#!/usr/bin/env python
import RPi.GPIO as GPIO

ON_PIN = 20
DIR_PIN = 20

# Initialize to LOW
GPIO.setup(ON_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(DIR_PIN, GPIO.OUT, initial=GPIO.LOW)

def turnOn(color):
    if color<0:
        GPIO.output(DIR_PIN, GPIO.HIGH)
    else:
        GPIO.output(DIR_PIN, GPIO.LOW)
    GPIO.output(ON_PIN, GPIO.HIGH)

def turnOff():
    GPIO.output(ON_PIN, GPIO.LOW)
    
def isOn():
    #TODO

def reset():
    GPIO.output(DIR_PIN, GPIO.LOW)
    GPIO.output(ON_PIN, GPIO.LOW)