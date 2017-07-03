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
def setStep(step, mot):
	p = pins[mot]
	for i in range(0,4):
		GPIO.output(p[i], step[i])
def forward(delay, steps, mot):  
	for i in range(0, steps):
		for j in range(0, len(seq)):
			setStep(seq[j], mot)
			time.sleep(delay)
def backwards(delay, steps, mot):
	for i in range(0, steps):
		for j in range(0, len(seq)):
			setStep(seq[len(seq)-j-1], mot)
			time.sleep(delay)

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
