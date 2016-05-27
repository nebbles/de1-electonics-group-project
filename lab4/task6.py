#_________________________________________________
#  Task 6: Function to generate UART sequence for '#' on Y1
#  initialize UART(6) to output TX on Pin Y1

import pyb
from pyb import Pin, Timer, UART
print('Task 6: Using UART to send "#"')

uart = UART(6)
while True:
	uart.init(9600, bits=8, parity = 0, stop = 2)
	uart.writechar(ord('#'))
	pyb.delay(5)
