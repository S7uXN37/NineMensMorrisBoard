import RPi.GPIO as GPIO
import time
usleep = lambda x: time.sleep(x/1000.0/1000.0)

# Mot1 on board, Mot2 below
triggerPin = [38,40]
triggerSet = [False, False]

def trigger0(channel):
	triggerSet[0]=True
def trigger1(channel):  
        triggerSet[1]=True

GPIO.setmode(GPIO.BOARD)

# Initialize to LOW
GPIO.setup(triggerPin[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(triggerPin[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(triggerPin[0], GPIO.RISING, callback=trigger0)
GPIO.add_event_detect(triggerPin[1], GPIO.RISING, callback=trigger1)
# UI
try:
	while True:
		print(triggerSet)
except KeyboardInterrupt:
	print("\nResetting...")
	# forward until signal
	for i in range(2):
		triggerSet[i] = (GPIO.input(triggerPin[i]) == 1)
	print(triggerSet)
	while not (triggerSet[0] and triggerSet[1]):
		xy = [0 if triggerSet[0] else -1, 0 if triggerSet[1] else -1]
		print(xy)
	print("\nDone. Closing...")

GPIO.cleanup()
print("Cleaned up")
