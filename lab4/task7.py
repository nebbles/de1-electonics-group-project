print('This is Task 7: Sending text messages to phone via bluetooth')
import pyb
from pyb import Pin, Timer, UART

# LE 2708 is our bluetooth module

the_word = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
#  initialize UART(6) to output TX on Pin Y1
uart = UART(6)
uart.init(9600, bits=8, parity = None, stop = 2)
while True:
	for i in range(36):
		uart.writechar(ord(the_word[i]))
	uart.writechar(13)
	uart.writechar(10)
	pyb.delay(1000)
