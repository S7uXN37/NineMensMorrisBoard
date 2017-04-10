import RPi.GPIO as GPIO
from time import sleep

# GLOBALS
pin = 35
value = 0

# ----- PROGRAM ------

GPIO.setmode(GPIO.BOARD)

# Initialize to LOW
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Callback
def myCallback(channel):
	global value
	value += 1
GPIO.add_event_detect(pin, GPIO.RISING, callback=myCallback)

# UI
try:
	while True:
		print("Read: ", value)
		value = 0
		sleep(0.2)
except KeyboardInterrupt:
	print("\nClosing...")
finally:
	GPIO.cleanup()
	print("Cleaned up")

