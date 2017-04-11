import RPi.GPIO as GPIO
import threading
import time
import math

class Motor():
    def __init__(self, pins):
        print("Creating Motor with pins: ", pins)
        self.pins = pins
    def startMove(self, cycles):
        print("Creating new MotorThread for pins: ", self.pins)
        self.thread = MotorThread(self.pins)
        self.thread.startMove(math.abs(cycles), math.sign(cycles))
    def stop(self):
        print("Stopping thread with pins: ", self.pins)
        self.thread.stop()
class MotorThread(threading.Thread):
    delay = 1.8
    seq = [[0,0,1,1],
            [1,0,0,1],
            [1,1,0,0],
            [0,1,1,0]]
    
    def setStep(step, pins):
        print(step)
        for i in range(0,4):
            GPIO.output(pins[i], step[i])
    
    def __init__(self, pins):
        super(MotorThread, self).__init__()
        self.daemon = True
        
        self._stop = threading.Event()
        self._pins = pins
        self._steps = 0
        self._direction = 1
    def startMove(self, steps, direction):
        self._steps = steps
        self._direction = direction
        self._stop.clear()
        self.start()
    def stop(self):
        self._stop.set()
    def run(self):
        global seq, setStep, delay
        for i in range(0, self._steps):
            for j in range(0, len(seq)):
                setStep(self._direction * seq[j], pins)
                time.sleep(delay)
                if self._stop.isset():
                    print("MotorThread received STOP, returning...")
                    return
            
# PIN_A, PIN_B, PIN_C, PIN_D
pins = [[35,31,33,29], [35,31,33,29]] # PINS_X, PINS_Y
calibs = [7, 8] # CALIB_X, CALIB_Y
cm_per_cycle = 0.0754
cm_per_unit = 53.0/6
motor_x = Motor(pins[0])
motor_y = Motor(pins[1])
x = 0.0
y = 0.0

def calibMotor(channel):
    if calibs[0] == channel:
        print("X-Motor calibrated")
        motor_x.stop()
    elif calibs[1] == channel:
        print("Y-Motor calibrated")
        motor_y.stop()

def toCycles(delta):
    return delta * cm_per_unit / cm_per_cycle
    
def moveTo(t_x, t_y):
    global x, y
    # Start threads
    if t_x == 0 and t_y == 0: #Recalibrate -> run until stopped by CALIB
        print("Calibrating...")
        motor_x.startMove(100000, -1)
        motor_y.startMove(100000, -1)
    else:
        print("Moving...")
        motor_x.startMove(toCycles(t_x - x))
        motor_y.startMove(toCycles(t_y - y))
    # Wait for threads to finish
    motor_x.thread.join()
    motor_y.thread.join()
    # Set new position
    x = t_x
    y = t_y

print("Setting up motors...")
GPIO.setmode(GPIO.BOARD)
for pin in pins[0]:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
for pin in pins[1]:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
for pin in calibs:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=calibMotor)
print("Motor setup completed!")
moveTo(0,0)