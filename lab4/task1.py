import pyb
from pyb import Pin, Timer

# Task 1: Blink LEDs in 1 second intervals
print('This is Task 1: Blink LEDs in 1 second intervals')

rLED = Pin('Y9', Pin.OUT_PP)
yLED = Pin('Y10', Pin.OUT_PP)

while True:
    rLED.high()
    pyb.delay(250) #delay of 250 millisec
    yLED.high()
    pyb.delay(250)
    rLED.low()
    pyb.delay(250)
    yLED.low()
    pyb.delay(250)
