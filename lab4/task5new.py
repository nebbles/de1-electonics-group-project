#_________________________________________________
# Task 5: Testing the ultrasound range sensor  V2
#  Robust version: Peter Cheung, suggested by James Davis
#  8th June 2016

import pyb
from pyb import Pin, Timer
print('Task 5: Test the Ultrasound distance sensor')

Trigger = Pin('X3', Pin.OUT_PP)
Echo = Pin('X4',Pin.IN)
	
# Create a microseconds counter.
micros = pyb.Timer(5, prescaler=83, period=0x3fffffff) #** Use timer 5 instead of 2
micros.counter(0)

TIME_OUT_1 = 2000		#** maximum delay for echo signal to go high
TIME_OUT_2 = 29000		#** maximum pulse width equal 5m distance
	
while True:
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
	pyb.delay(500)