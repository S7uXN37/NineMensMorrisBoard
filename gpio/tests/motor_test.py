import RPi.GPIO as GPIO
import time
usleep = lambda x: time.sleep(x/1000.0/1000.0)

dirPin = 33
stepPin = 35
sleepPin = 36
delay = 1800.0

def move(steps, dir):
	GPIO.output(dirPin, GPIO.HIGH if dir>0 else GPIO.LOW)
	GPIO.output(sleepPin, GPIO.HIGH)
	for i in range(0, steps):
		GPIO.output(stepPin, GPIO.HIGH)
		usleep(1)
		GPIO.output(stepPin, GPIO.LOW)
		t = 400.0
		d_start = 4000.0
		f_i = (d_start-delay)/(t*t) * (i-t)*(i-t) + delay
		usleep(f_i if i < t else delay)
	GPIO.output(sleepPin, GPIO.LOW)

GPIO.setmode(GPIO.BOARD)

# Initialize to LOW
for pin in [dirPin, stepPin, sleepPin]:
	GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

# UI
try:
	if int(raw_input("Loop or Manual (1/0)?")) > 0:
		while True:
			move(2200, 1)
			time.sleep(0.5)
			move(2200,0)
			time.sleep(0.5)
	else:
		while True:
			steps = raw_input("How many steps forward? ")
			move(int(steps), 1)
			steps = raw_input("How many steps backwards? ")
			move(int(steps), 0)
except KeyboardInterrupt:
	print("\nClosing...")

GPIO.output(sleepPin, GPIO.LOW)

GPIO.cleanup()
print("Cleaned up")
