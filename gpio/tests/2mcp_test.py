from gpiozero import MCP3008
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
cs = [24, 25]
for c in cs:
    GPIO.setup(c, GPIO.OUT, initial=GPIO.HIGH)

try:
    while True:
        vals=[x for x in range(8)]
        y = ""
        for val in vals:
            y += str(MCP3008(channel=val, port=0, device=1).value)
            #y += str(pot.value) + "        "
        print(y)
except KeyboardInterrupt:
    quit(0)
