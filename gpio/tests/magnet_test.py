import RPi.GPIO as GPIO
import time

pinA = 13
pinB = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup([pinA, pinB], GPIO.OUT, initial=GPIO.LOW)

def set(dir):
	if dir == 0:
		GPIO.output(pinA, GPIO.LOW)
		GPIO.output(pinB, GPIO.LOW)
	elif dir > 0:
		GPIO.output(pinA, GPIO.HIGH)
		GPIO.output(pinB, GPIO.LOW)
	else:
		GPIO.output(pinA, GPIO.LOW)
		GPIO.output(pinB, GPIO.HIGH)

try:
	i = 0
	while True:
		#dir = int(raw_input("Direction: "))
		dir = 1#i%3 -1
		set(dir)
		print(dir)
		time.sleep(1)
		i+=1
except KeyboardInterrupt:
	GPIO.output([pinA, pinB], GPIO.LOW)
	GPIO.cleanup()
