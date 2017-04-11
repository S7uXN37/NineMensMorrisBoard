import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
pin = 7
GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

try:
	i = 10
	while i > 0:
		print i
		secs = i * 0.02
		GPIO.output(pin, GPIO.HIGH)
		time.sleep(secs)
		GPIO.output(pin, GPIO.LOW)
		time.sleep(secs)
		i-=1
finally:
	GPIO.output(pin, GPIO.LOW)
	GPIO.cleanup()
