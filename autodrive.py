print('Initialising Autodrive Module')
print('Version 1.0')

from pyb import Pin, ADC, Timer

# Key variables --------------------------------------------------
speed = 50 # standard driving speed
critdistance = 30 # critical stopping distance in cm


# Defining the motor modules--------------------------------------
A1 = Pin('Y9',Pin.OUT_PP)
A2 = Pin('Y10',Pin.OUT_PP)
motor1 = Pin('X1')

B1 = Pin('Y11',Pin.OUT_PP)
B2 = Pin('Y12',Pin.OUT_PP)
motor2 = Pin('X2')

tim = Timer(2, freq = 1000)
ch1 = tim.channel(1, Timer.PWM, pin = motor1)
ch2 = tim.channel(2, Timer.PWM, pin = motor2)

# Ultrasound Echo Initialising -----------------------------------
Trigger = Pin('X3', Pin.OUT_PP)
Echo = Pin('X4',Pin.IN)
# Create a microseconds counter.
micros = pyb.Timer(5, prescaler=83, period=0x3fffffff)
micros.counter(0)
start = 0				# timestamp at rising edge of echo
end = 0					# timestamp at falling edge of echo

# -----------------------------------------------------------------

def drive(speed): # Set direction to forward

	A1.high()
	A2.low()

	B1.low()
	B2.high()

	ch1.pulse_width_percent(speed) # send a pulse of width 50% to motor1
	ch2.pulse_width_percent(speed) # send a pulse of width 50% to motor2

def preventCollision(speed):

	# slowdown
	while speed > 0:
		speed = speed - 5
		ch1.pulse_width_percent(speed)
	 	ch2.pulse_width_percent(speed)
		pyb.delay(50) # delay for 50 millisec

	# stop
	ch1.pulse_width_percent(0)
	ch2.pulse_width_percent(0)

	# reverse both motor direction
	A1.low()
	A2.high()

	B1.high()
	B2.low()

	# set motor1: 15%, motor2: 15%
	# motor direction has already been reversed
	# pulse width cannot be negative
	ch1.pulse_width_percent(40)
	ch2.pulse_width_percent(40)

	# run to allow reverse
	pyb.delay(3500) # x millisec

	# turn on the spot 
	ch1.pulse_width_percent(0)
	ch2.pulse_width_percent(40)

	# run to allow the turn
	pyb.delay(1250)
	
	# stop
	ch1.pulse_width_percent(0)
	ch2.pulse_width_percent(0)

	pyb.delay(1000)
	# run drive(at 50%) func (which should correct the motor direction)
	drive(50)

drive(speed) # begin the drive

while True: # Distance feedback loop
	# Send a 20usec pulse every 10ms
	Trigger.high()
	pyb.udelay(20) #udelay uses argument in microseconds
	Trigger.low()

	# Wait until echo pulse goes from low to high
	while Echo.value() == 0:
		start = micros.counter()	# record start time of pulse

	# Wait until echo pulse goes from high to low
	while Echo.value() == 1:   # do nothing
		end = micros.counter()		# record end time of pulse

	# Calculate distance from delay duration
	distance = int(((end - start) / 2) / 29) # distance in cm
	print('Distance: ', distance, ' cm')

	if distance <= critdistance:
		preventCollision(speed)

	pyb.delay(500) # delay 500 millisec before repeating loop
