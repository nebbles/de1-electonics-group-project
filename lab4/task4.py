# Task 4: Joystick Controlling the Motor
# Author: BSG
# Version 1.0
# 26 May 2016

print ('This is Test 4: Joystick Controlling the Motor')
from pyb import Pin, Timer, ADC



while True:
    pyb.delay(1)
    A1 = Pin('Y9',Pin.OUT_PP)
    A2 = Pin('Y10',Pin.OUT_PP)
    A1.high()
    A2.low()
    motor = Pin('X1')
    tim = Timer(2, freq = 1000)
    ch = tim.channel(1, Timer.PWM, pin = motor)



    adc_1 = ADC(Pin('X19')) #vertical
    adc_2 = ADC(Pin('X20')) #horizontal
    J_sw = Pin('Y11', Pin.IN) #switch

    vertical = (int(adc_2.read()) / 1700)*100
    ch.pulse_width_percent(vertical)
