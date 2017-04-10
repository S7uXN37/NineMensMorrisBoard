import RPi.GPIO as GPIO 
import time

GPIO.setmode(GPIO.BCM) 
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def buttonPress(channel): 
    print "Button pressed!"

GPIO.add_event_detect(24, GPIO.RISING, callback=buttonPress, bouncetime=300)

print("Listening...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()           # clean up GPIO on normal exit 
