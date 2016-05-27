print('This is Task 5: Ultrasound distance sensor')
#_________________________________________________
# Task 5: Testing the ultrasound range sensor

import pyb
from pyb import Pin, Timer


Trigger = Pin('X3', Pin.OUT_PP)
Echo = Pin('X4',Pin.IN)

# Create a microseconds counter.
micros = pyb.Timer(2, prescaler=83, period=0x3fffffff)
micros.counter(0)
start = 0				# timestamp at rising edge of echo
end = 0					# timestamp at falling edge of echo

while True:
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
	distance = int(((end - start) / 2) / 29)
	print('Distance: ', distance, ' cm')
	pyb.delay(500)
