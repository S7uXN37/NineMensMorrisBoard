import RPi.GPIO as GPIO
from time import sleep

# GLOBALS

# ----- PROGRAM ------

GPIO.setmode(GPIO.BOARD)

# UI
try:
	GPIO.setup(31, GPIO.OUT)
	GPIO.setup(35, GPIO.OUT)
	GPIO.setup(33, GPIO.OUT)
	GPIO.setup(37, GPIO.OUT)
	while True:
		secs = int(raw_input("Seconds: "))
		GPIO.output(31, GPIO.HIGH)
		GPIO.output(35, GPIO.HIGH)
		sleep(secs)
		GPIO.output(31, GPIO.LOW)
		GPIO.output(35, GPIO.LOW)
except KeyboardInterrupt:
	print("\nClosing...")
finally:
	GPIO.output(31, GPIO.LOW)
	GPIO.output(33, GPIO.LOW)
	GPIO.output(35, GPIO.LOW)
	GPIO.output(37, GPIO.LOW)
	GPIO.cleanup()
	print("Cleaned up")
