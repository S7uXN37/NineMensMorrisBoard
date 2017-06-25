import RPi.GPIO as GPIO
import time

# GLOBALS
# PIN_A, PIN_B, PIN_C, PIN_D
pins = [35,31,33,29]
seq = [[0,0,1,1],
	[1,0,0,1],
	[1,1,0,0],
	[0,1,1,0]]

def setStep(step):
	print(step)
	for i in range(0,4):
		GPIO.output(pins[i], step[i])


def forward(delay, steps):  
	for i in range(0, steps):
		for j in range(0, len(seq)):
			setStep(seq[j])
			time.sleep(delay)

def backwards(delay, steps):
	for i in range(0, steps):
		for j in range(0, len(seq)):
			setStep(seq[len(seq)-j-1])
			time.sleep(delay)

# ----- PROGRAM ------

GPIO.setmode(GPIO.BOARD)

# Initialize to LOW
for pin in pins:
	GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

def reset():
	for pin in pins:
		GPIO.output(pin, GPIO.LOW)