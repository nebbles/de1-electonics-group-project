# ----------------------------------------------------
#  Task 8: Get keypad commands via Bluetooth

import pyb
from pyb import Pin, Timer, UART
print('Task 8: Test keypad communication with Pyboard')

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
