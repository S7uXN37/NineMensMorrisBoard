import RPi.GPIO as GPIO
import time

# GLOBALS
# PIN_A, PIN_B, PIN_C, PIN_D
pins = [[29,33,31,35],
    [32,38,36,40]]
seq = [[0,0,1,1],
    [1,0,0,1],
    [1,1,0,0],
    [0,1,1,0]]
coordToSteps = 1.0
DELAY = 0.005
px = 0.0
py = 0.0


def setStep(step, mot):
    p = pins[mot]
    for i in range(0,4):
        GPIO.output(p[i], step[i])


def move(delay, steps, mot):
    if steps > 0:
        for i in range(0, steps):
            for j in range(0, len(seq)):
                setStep(seq[j], mot)
    else:
        steps = -steps
        for i in range(0, steps):
            for j in range(0, len(seq)):
                setStep(seq[len(seq)-j-1], mot)
    time.sleep(delay)


def goTo(tx, ty):
    x = (float(tx) - px) * coordToSteps
    y = (float(ty) - py) * coordToSteps
    move(DELAY, x, 0)
    move(DELAY, y, 1)

# ----- PROGRAM ------

GPIO.setmode(GPIO.BOARD)

# Initialize to LOW
for p in pins:
    for pin in p:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)


def reset():
    for p in pins:
        for pin in p:
            GPIO.output(pin, GPIO.LOW)