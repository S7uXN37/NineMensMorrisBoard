import RPi.GPIO as GPIO
import time
import threading
usleep = lambda x: time.sleep(x/1000.0/1000.0)

coordToSteps = 2000.0 / 6.0
RESET_POS = [-0.22, -0.64] # 6.6cm/grid -4cm/6.6=-0.6, -1.5cm/6.6=-0.22

# Mot1 on board, Mot2 below
dirPin = [29,33]
stepPin = [31,35]
sleepPin = [32,36]
triggerPin = [16,40]
triggerSet = [False, False]
delay = 1800.0

def daemon():
    c = 0
    while True:
        time.sleep(0.01)
        if GPIO.input(triggerPin[0]) == 1:
            c += 1
        else:
            c = 0
        if c == 5:
            triggerSet[0] = True
def trigger1(channel):
    triggerSet[1]=True

def move(steps):
    for j in range(2):
        GPIO.output(dirPin[j], GPIO.HIGH if steps[j]<0 else GPIO.LOW)
        GPIO.output(sleepPin[j], GPIO.HIGH)
        steps[j] = abs(steps[j])
    time.sleep(0.15)
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
    time.sleep(0.1)
    for j in range(2):
        GPIO.output(sleepPin[j], GPIO.LOW)

GPIO.setmode(GPIO.BOARD)

# Initialize to LOW
for pin in [dirPin, stepPin, sleepPin]:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(triggerPin[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(triggerPin[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
d = threading.Thread(name='Daemon', target=daemon)
d.setDaemon(True)
d.start() # Event detect doesn't work because of fluctuations
GPIO.add_event_detect(triggerPin[1], GPIO.RISING, callback=trigger1)

posx = 0
posy = 0

def goTo(tx, ty):
    global posx, posy
    x = int((tx - posx) * coordToSteps)
    y = int((ty - posy) * coordToSteps)
    print("Moving from " + str((posx,posy)) + " to " + str((tx,ty)))
    move([x,y])
    posx = tx  # Must be in simple coordinate system!
    posy = ty

def reset():
    goTo(RESET_POS[0], RESET_POS[1])
    global posx, posy
    posx = RESET_POS[0]
    posy = RESET_POS[1]
    for i in range(2):
        triggerSet[i] = (GPIO.input(triggerPin[i]) == 1)
    while not (triggerSet[0] and triggerSet[1]):
        xy = [0 if triggerSet[0] else -10, 0 if triggerSet[1] else -10]
        move(xy)

def shutdown():
    GPIO.output(sleepPin[0], GPIO.LOW)
    GPIO.output(sleepPin[1], GPIO.LOW)
