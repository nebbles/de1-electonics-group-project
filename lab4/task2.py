#Task 2: motor control
print('This is Task 2: Motor Control')

from pyb import Pin, Timer

A1 = Pin('Y9',Pin.OUT_PP)
A2 = Pin('Y10',Pin.OUT_PP)

A1.high()
A2.low()

motor = Pin('X1')
tim = Timer(2, freq = 1000)
ch = tim.channel(1, Timer.PWM, pin = motor)

ch.pulse_width_percent(50)
