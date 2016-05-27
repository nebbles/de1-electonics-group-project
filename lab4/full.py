#  Program that provides solutions to the different tasks
#  in Lab Session 4
#  Written by: Peter Cheung  Version: 1.0  22 May 2016

import pyb
from pyb import Pin, Timer, UART, ADC

#_________________________________________________
# Task 1: Blink LEDs NTIMES times
def	flash_LEDs():

	rLED = Pin('Y9', Pin.OUT_PP)
	bLED = Pin('Y10',Pin.OUT_PP)

	while True:
		rLED.high()
		pyb.delay(250)
		bLED.high()
		pyb.delay(250)
		rLED.low()
		pyb.delay(250)
		bLED.low()
		pyb.delay(250)
	
#_________________________________________________
# Task 2: Drive motor with PWM signal produced on X1
def  drive_motor():
	A1 = Pin('Y9',Pin.OUT_PP)
	A2 = Pin('Y10',Pin.OUT_PP)
	A1.high()
	A2.low()
	motor = Pin('X1')
	tim = Timer(2, freq = 1000)
	ch = tim.channel(1, Timer.PWM, pin = motor)
	while True:
		ch.pulse_width_percent(50)
	
#_________________________________________________
# Task 3: Use ADC to measure joystick reading
def check_joystick():

	adc_1 = ADC(Pin('X19'))
	adc_2 = ADC(Pin('X20'))
	J_sw = Pin('Y11', Pin.IN)

	while True:
		print('Vertical: ',adc_1.read(), 'Horizontal: ', adc_2.read(), 'Switch: ',J_sw.value())
		pyb.delay(2000)	
		
#_________________________________________________
# Task 4: Use joystick to control motor
def motor_control():
	# define various I/O pins for ADC
	adc_1 = ADC(Pin('X19'))
	adc_2 = ADC(Pin('X20'))

	# set up motor with PWM and timer control
	A1 = Pin('Y9',Pin.OUT_PP)
	A2 = Pin('Y10',Pin.OUT_PP)
	pwm_out = Pin('X1')
	tim = Timer(2, freq = 1000)
	motor = tim.channel(1, Timer.PWM, pin = pwm_out)
	
	A1.high()	# motor in brake position
	A2.high()

	# Calibrate the neutral position for joysticks
	MID = adc_1.read()		# read the ADC 1 value now to calibrate
	DEADZONE = 10	# middle position when not moving
	
	# Use joystick to control forward/backward and speed
	while True:				# loop forever until CTRL-C
		speed = int(100*(adc_1.read()-MID)/MID)
		if (speed >= DEADZONE):		# forward
			A1.high()
			A2.low()
			motor.pulse_width_percent(speed)
		elif (speed <= -DEADZONE):
			A1.low()		# backward
			A2.high()
			motor.pulse_width_percent(-speed)
		else:
			A1.low()		# stop
			A2.low()		

#_________________________________________________
# Task 5: Testing the ultrasound range sensor
def	ultrasound():
	
	Trigger = Pin('X3', Pin.OUT_PP)
	Echo = Pin('X4',Pin.IN)
	
	# Create a microseconds counter.
	micros = pyb.Timer(2, prescaler=83, period=0x3fffffff)
	micros.counter(0)
	start = 0
	end = 0
	
	# Send a 20usec pulse every 10ms
	while True:
		Trigger.high()
		pyb.udelay(20)
		Trigger.low()
		
		# Wait until pulse starts
		while Echo.value() == 0:   # do nothing
			start = micros.counter()	# mark time at rising edge
		
		# Wait until pulse goes low
		while Echo.value() == 1:   # do nothing
			end = micros.counter()		# mark time at falling edge
		
		# Duration echo pulse = end - start
		# Divide this by 2 to take account of round-trip
		# Speed of sound in air is 340 m/s or 29 us/cm
		# Distance in cm = (pulse_width)*0.5/29
		distance = int(((end - start) / 2) / 29)
		print('Distance: ', distance, ' cm')
		pyb.delay(500)

#_________________________________________________
#  Task 6: Function to generate UART sequence for '#' on Y1
def  uart_hash():
	#  initialize UART(6) to output TX on Pin Y1
	uart = UART(6)
	while True:
		uart.init(9600, bits=8, parity = 0, stop = 2)
		uart.writechar(ord('#'))		# letter '#'
		pyb.delay(5)					# delay by 5ms

# ----------------------------------------------------
#  Task 7: Send continuous #FOG to phone via bluetooth
def  uart_hashtag():
	the_word = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	#  initialize X5 as  trigger output
	uart = UART(6)
	uart.init(9600, bits=8, parity = None, stop = 2)
	while True:
	#  initialize UART(6) to output TX on Pin Y1
		for i in range(36):
			uart.writechar(ord(the_word[i]))
		uart.writechar(13)
		uart.writechar(10)
		pyb.delay(1000)
		
# ----------------------------------------------------
#  Task 8: Get keypad commands via Bluetooth
def  keypad():
	key = ('1','2','3','4','U','D','L','R')
	uart = UART(6)
	uart.init(9600, bits=8, parity = None, stop = 2)
	while True:
		while (uart.any()!=10):    #wait we get 10 chars
			n = uart.any()
		command = uart.read(10)
		key_index = command[2]-ord('1')
		if (0 <= key_index <= 7) :
			key_press = key[key_index]
		if command[3]==ord('1'):
			action = 'pressed'
		elif command[3]==ord('0'):
			action = 'released'
		else:
			action = 'nothing pressed'
		print('Key',key_press,' ',action)
					
# ----------------------------------------------------
#  Task 9: Use phone to control motor via Bluethooth
def  remote():

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

# ----------------------------------------------------
#  Prompt for task no
while True:
	print('\n---- Compbined solution for Lab 4 ----')
	print('Task 1: Flashing LEDs at 1 second period')
	print('Task 2: Run motor at specified speed')
	print('Task 3: Joystick feeding ADC')
	print('Task 4: Use Joystick to control motor speed')
	print('Task 5: Test the Ultrasound distance sensor')
	print('Task 6: Using UART to send "#"')
	print('Task 7: Send 26 alphabets and 10 digits to phone')
	print('Task 8: Test keypad communication with Pyboard')
	print('Task 9: Keypad controlling motor')
	print('\n')

	task =  int(input("Enter Task (Ctrl-C to exit task):"))

	if task == 1:
		print ('Task 1: flashing LEDs\n')
		flash_LEDs()	
	elif task == 2:
		print ('Task 2: Driving dc motor\n')
		drive_motor()
	elif task == 3:
		print ('Task 3: Testing joystick\n')
		check_joystick()
	elif task == 4:
		print ('Task 4: Control motor speed with joystick\n')
		motor_control()
	elif task == 5:
		print ('Task 5: Test Ultrasound distance sensor\n')
		ultrasound()
	elif task == 6:
		print ('Task 6: Using the UART on Pyboard to send ASCI character to Y1\n')
		uart_hash()
	elif task == 7:
		print ('Task 7: Sending 26 alphabets and 10 digits to phone via Bluetooth\n')
		uart_hashtag()
	elif task == 8:
		print ('Task 8: Test keypad communication with Pyboard\n')
		keypad()
	elif task == 9:
		print ('Task 9: Control motor speed with keypad\n')
		remote()
