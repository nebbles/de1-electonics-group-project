print('Initialising Autodrive Module')
print('Version 1.0')

from pyb import Pin, ADC, Timer

# Key variables --------------------------------------------------
speed = 50 # standard driving speed
critdistance = 40 # critical stopping distance in cm


# Defining the motor modules--------------------------------------
A1 = Pin('Y9',Pin.OUT_PP) # motor A is on the RHS of the vehicle
A2 = Pin('Y10',Pin.OUT_PP)
motor1 = Pin('X1')

B1 = Pin('Y11',Pin.OUT_PP) # motor B is on the LHS of the vehicle
B2 = Pin('Y12',Pin.OUT_PP)
motor2 = Pin('X2')

tim = Timer(2, freq = 1000)
ch1 = tim.channel(1, Timer.PWM, pin = motor1)
ch2 = tim.channel(2, Timer.PWM, pin = motor2)

# Ultrasound Echo Initialising -----------------------------------
Trigger = Pin('X3', Pin.OUT_PP)
Echo = Pin('X4',Pin.IN)

# Create a microseconds counter.
micros = pyb.Timer(5, prescaler=83, period=0x3fffffff) #** Use timer 5 instead of 2
micros.counter(0)

TIME_OUT_1 = 2000		#** maximum delay for echo signal to go high
TIME_OUT_2 = 29000		#** maximum pulse width equal 5m distance

# -----------------------------------------------------------------

def stop():
	ch1.pulse_width_percent(0) # send a pulse of width 0% to motor A
	ch2.pulse_width_percent(0) # send a pulse of width 0% to motor B

def drive(speed): # Set direction to forward

	A1.high() # Motor A set forward
	A2.low()

	B1.low() # Motor B set forward
	B2.high()

	ch1.pulse_width_percent(speed) # send a pulse of width 'speed'% to motor A
	ch2.pulse_width_percent(speed) # send a pulse of width 'speed'% to motor B

def preventCollision(speed):

	# slowdown
	while speed > 0:
		speed = speed - 5
		ch1.pulse_width_percent(speed)
	 	ch2.pulse_width_percent(speed)
		pyb.delay(50) # delay for 50 millisec

	stop() # stop

	# reverse both motor directions
	A1.low()
	A2.high()
	B1.high()
	B2.low()

	# reversing
	ch1.pulse_width_percent(40)
	ch2.pulse_width_percent(40)
	pyb.delay(750) # delay to allow reverse
	stop()
	pyb.delay(750) # pause before next command

	# set motor B (LHS) to forward
	B1.low()
	B2.high()

	# turn on the spot
	ch1.pulse_width_percent(40)
	ch2.pulse_width_percent(40)
	pyb.delay(500) # delay to allow the turn

	stop() # stop
	pyb.delay(500) # pause before continuing


drive(speed) # begin the drive - first line initiated on boot-up

while True: # Distance feedback loop
	# Send a 20usec pulse every 20ms
	micros.counter(0)	#** reset microsecond counter
	Trigger.high()
	pyb.udelay(20)
	Trigger.low()

	# Wait until echo pulse goes from low to high
	while Echo.value() == 0:
		if micros.counter() > TIME_OUT_1: 	#** maximum wait time is 2ms
			micros.counter(0)					#** reset microsecond counter
			Trigger.high()	#** trigger ultrasound sensor again!
			pyb.udelay(20)
			Trigger.low()

	micros.counter(0)	#** reset microsecond counter
	# Wait until echo pulse goes from high to low
	while Echo.value() == 1:   # do nothing
		pulse_width = micros.counter()		#** record end time of pulse
		if pulse_width > TIME_OUT_2:		#** check for time out again
			break			#** waited too long for falling edge

	# Calculate distance from delay duration
	distance = int((pulse_width/2) / 29)
	print('Echo pulse width:', pulse_width, 'Distance: ', distance, ' cm')

	if distance <= critdistance:
		preventCollision(speed)
	else:
		drive(50) # run drive(at 50%) func (it will set motor direction)

	pyb.delay(250) # delay by x millisec before repeating loop
