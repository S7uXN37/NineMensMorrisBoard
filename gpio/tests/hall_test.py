#import RPi.GPIO as GPIO
import fake_GPIO as GPIO
import matplotlib.pyplot as plt

# GLOBALS
pin = 35
value = 0

# SETUP
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setmode(GPIO.BOARD)

# UI
try:
    plt.axis([0, 10, 0, 1])
    plt.ion()
    
    x = 1
    last_y = 0
    
    while True:
        y = GPIO.input(pin)
        plt.scatter(x, y)
        plt.plot([x-1, x], [last_y, y], "-b")
        
        plt.pause(0.05)
        x += 1
        last_y = y
        
except KeyboardInterrupt:
	print("\nClosing...")
finally:
	GPIO.cleanup()
	print("Cleaned up")

