from pyb import Pin, Timer, ADC

print('This is Task 3: Joystick Feedback')

adc_1 = ADC(Pin('X19'))
adc_2 = ADC(Pin('X20'))

J_sw = Pin('Y11', Pin.IN)

while True:
    print('Vertical: ', adc_1.read(), 'Horizontal: ', adc_2.read(), 'Switch: ', J_sw.value())
    pyb.delay(100)
