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

def setStep(step):
	print(step)
	for p in pins:
		for i in range(0,4):
			GPIO.output(p[i], step[i])


def forward(delay, steps):  
	for i in range(0, steps):
		for j in range(0, len(seq)):
			setStep(seq[j])
			time.sleep(delay)
	setStep([0,0,0,0])

def backwards(delay, steps):
	for i in range(0, steps):
		for j in range(0, len(seq)):
			setStep(seq[len(seq)-j-1])
			time.sleep(delay)
	setStep([0,0,0,0])

# ----- PROGRAM ------

GPIO.setmode(GPIO.BOARD)

# Initialize to LOW
for pin in pins:
	GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

# UI
try:
	while True:
		delay = raw_input("Delay between steps (milliseconds)? ")
		steps = raw_input("How many steps forward? ")
		forward(float(delay) / 1000.0, int(steps))
		steps = raw_input("How many steps backwards? ")
		backwards(float(delay) / 1000.0, int(steps))
except KeyboardInterrupt:
	print("\nClosing...")
finally:
	for pin in pins:
		GPIO.output(pin, GPIO.LOW)
	GPIO.cleanup()
	print("Cleaned up")
