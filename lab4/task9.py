# ----------------------------------------------------
#  Task 9: Use phone to control motor via Bluethooth

import pyb
from pyb import Pin, Timer, ADC, UART
print('Task 9: Keypad controlling motor')

#initialise UART communication
uart = UART(6)
uart.init(9600, bits=8, parity = None, stop = 2)

# define various I/O pins for ADC
adc_1 = ADC(Pin('X19'))
adc_2 = ADC(Pin('X20'))

# set up motor with PWM and timer control
A1 = Pin('Y9',Pin.OUT_PP)
A2 = Pin('Y10',Pin.OUT_PP)
pwm_out = Pin('X1')
tim = Timer(2, freq = 1000)
motor = tim.channel(1, Timer.PWM, pin = pwm_out)

# Motor in idle state
A1.high()
A2.high()
speed = 0
DEADZONE = 5

# Use keypad U and D keys to control speed
while True:				# loop forever until CTRL-C
	while (uart.any()!=10):    #wait we get 10 chars
		n = uart.any()
	command = uart.read(10)
	if command[2]==ord('5'):
		if speed < 96:
			speed = speed + 5
			print(speed)
	elif command[2]==ord('6'):
		if speed > - 96:
			speed = speed - 5
			print(speed)
	if (speed >= DEADZONE):		# forward
		A1.high()
		A2.low()
		motor.pulse_width_percent(speed)
	elif (speed <= -DEADZONE):
		A1.low()		# backward
		A2.high()
		motor.pulse_width_percent(-speed)
	else:
		A1.low()		# idle
		A2.low()		
