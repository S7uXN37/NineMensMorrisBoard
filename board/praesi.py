import motors
import magnet
import time
print()
print()
print("move to 0,0! place white piece on 6,6!")
input("press ENTER for x-axis...")
motors.goTo(6,0)
input("press ENTER for y-axis...")
motors.goTo(6,6)
input("press ENTER for magnet action...")
magnet.turnOn(-1)
time.sleep(0.5)
motors.goTo(3,6)
time.sleep(0.5)
magnet.turnOff()
time.sleep(0.5)
motors.goTo(0,0)
time.sleep(0.5)
motors.reset()

