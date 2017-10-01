import RPi.GPIO as GPIO
import time
import random
usleep = lambda x: time.sleep(x/1000.0/1000.0)

# Mot1 on board, Mot2 below
dirPin = [29,33]
stepPin = [31,35]
sleepPin = [32,36]
triggerPin = [38,40]
triggerSet = [False, False]
delay = 1800.0

def trigger0(channel):
	triggerSet[0]=True
def trigger1(channel):  
        triggerSet[1]=True

def move(steps):
	for j in range(2):
		GPIO.output(dirPin[j], GPIO.HIGH if steps[j]<0 else GPIO.LOW)
		GPIO.output(sleepPin[j], GPIO.HIGH)
		steps[j] = abs(steps[j])
	for i in range(max(steps[0], steps[1])):
		for j in range(2):
			if i>=steps[j]:
				continue
			GPIO.output(stepPin[j], GPIO.HIGH)
			usleep(1)
			GPIO.output(stepPin[j], GPIO.LOW)
		t = 400.0 #steps until full speed
		d_start = 4000.0 #start delay
		f_i = (d_start-delay)/(t*t) * (i-t)*(i-t) + delay #calc delay
		usleep(f_i if i < t else delay)
	for j in range(2):
		GPIO.output(sleepPin[j], GPIO.LOW)

GPIO.setmode(GPIO.BOARD)

# Initialize to LOW
for pin in [dirPin, stepPin, sleepPin]:
	GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(triggerPin[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(triggerPin[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(triggerPin[0], GPIO.RISING, callback=trigger0)
GPIO.add_event_detect(triggerPin[1], GPIO.RISING, callback=trigger1)
# UI
try:
	i = int(raw_input("Loop or Manual or Random (1/0/-1)?"))
	if i > 0:
		while True:
			x = 2000
			y = 2000
			move([x, y])
			time.sleep(0.5)
			move([-x, -y])
			time.sleep(0.5)
	elif i == 0:
		while True:
			steps = int(raw_input("How many steps forward? "))
			move([steps,steps])
			steps = int(raw_input("How many steps backwards? "))
			move([-steps,-steps])
	else:
		pos = [0,0]
		w = 2000.0
		while True:
			tx = int(random.random()*7.0)*w/6.0
			ty = int(random.random()*7.0)*w/6.0
			dx = int(tx-pos[0])
			dy = int(ty-pos[1])
			print(str(tx) + "/" + str(ty))
			move([dx,dy])
			pos[0] = pos[0]+dx
			pos[1] = pos[1]+dy
except KeyboardInterrupt:
	print("\nResetting...")
	# forward until signal
	for i in range(2):
		triggerSet[i] = (GPIO.input(triggerPin[i]) == 1)
	print(triggerSet)
	while not (triggerSet[0] and triggerSet[1]):
		xy = [0 if triggerSet[0] else -1, 0 if triggerSet[1] else -1]
		print(xy)
		move(xy)
	print("\nDone. Closing...")

GPIO.output(sleepPin[0], GPIO.LOW)
GPIO.output(sleepPin[1], GPIO.LOW)
str = raw_input("\nDone, sleeping; turn off power!\nPress any key to continue...")

GPIO.cleanup()
print("Cleaned up")
