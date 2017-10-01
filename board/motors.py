import RPi.GPIO as GPIO
import time

coordToSteps = 2000.0 / 6.0

# GLOBALS

# def move

def goTo(tx, ty):
    x = int((float(tx) - posx) * coordToSteps)
    y = int((float(ty) - posy) * coordToSteps)
    move([x,y])

# ----- PROGRAM ------

GPIO.setmode(GPIO.BOARD)

# Initialize to LOW
for p in pins:
    for pin in p:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

# TODO hookPressure

def reset():
    for p in pins:
        for pin in p:
            GPIO.output(pin, GPIO.LOW)