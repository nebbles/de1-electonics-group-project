# Pilot script to control robot via bluetooth

print('Initialising Pilot Module')
print('Version 0.1')

from pyb import Pin, ADC, Timer, UART

# Key global variables
direction = 'f'
speedL = 0
speedR = 0
critdistance = 30

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
# initialise UART communication
uart = UART(6)
uart.init(9600, bits=8, parity = None, stop = 2)
# -----------------------------------------------------------------

def direction(direction, speedL, speedR):
    # if speed is not zero then the car should stop first
    # slowdown not possible yet with L and R
    # we therefore call the stop function to stop for us
    (speedL, speedR) = stop()

    if direction == 'f':
    	A1.high()
    	A2.low()

    	B1.low()
    	B2.high()

        direction = 'f'
        #return 'f'

    elif direction == 'b':
    	A1.low()
    	A2.high()

    	B1.high()
    	B2.low()
        direction = 'b'
        #return 'b'

    print('Direction changed to: ',direction)
    return (direction, speedL, speedR)

def speed(mode, speedL, speedR):
    if mode == 'inc':
        if speedL < 96 and speedR < 96:
            speedL += 5
            speedR += 5

    elif mode == 'dec':
        if speedL > 4 and speedR > 4:
            speedL -= 5
            speedR -= 5

    setspeed(speedL,speedR)
    return (speedL,speedR)

def stop():
    speedL = 0
    speedR = 0
    A1.low()
    A2.low()
    B1.low()
    B2.low()

    setspeed(speedL,speedR)
    return (speedL, speedR)

def setspeed(speedL,speedR):
    	ch1.pulse_width_percent(speedL) # send a pulse of width 50% to motor1
    	ch2.pulse_width_percent(speedR) # send a pulse of width 50% to motor2

def turn(turnDirection, speedL, speedR):
    if turnDirection == 'l':
        if speedL > 4 and speedR <96:
            speedL -= 5
            speedR += 5

    elif turnDirection == 'r':
        if speedL <96 and speedR >4:
            speedL += 5
            speedR -= 5

    setspeed(speedL,speedR)
    return (speedL,speedR)


# loop
# Use keypad controller to control car
while True:				# loop forever until CTRL-C
    while (uart.any()!=10):    #wait we get 10 chars
        n = uart.any()
    command = uart.read(10)
    if command[2] == ord('1'): # record
        print('Command not available yet')

    elif command[2] == ord('2'): # play
        print('Command not available yet')

    elif command[2] == ord('3'): # change direction
        print('Changing direction...')
        if direction == 'f':
            (direction,speedL,speedR) = direction(direction='b',speedL=speedL,speedR=speedR)
            print('SpeedL=',speedL,'SpeedR=',speedR,'Direction=',direction)
        elif direction == 'b':
            (direction,speedL,speedR) = direction(direction='f',speedL=speedL,speedR=speedR)
            print('SpeedL=',speedL,'SpeedR=',speedR,'Direction=',direction)

    elif command[2] == ord('4'): # emergency stop
        print('Stopping...')
        (speedL,speedR) = stop()
        print(speedL,speedR)

    elif command[2] == ord('5'): # UP pressed
        print('Increasing speed...')
        (speedL,speedR) = speed(mode=inc,speedL=speedL,speedR=speedR)
        print(speedL,speedR,direction)

    elif command[2] == ord('6'): # DOWN PRESSED
        print('Decreasing speed...')
        (speedL,speedR) = speed(mode=dec,speedL=speedL,speedR=speedR)
        print(speedL,speedR,direction)

    elif command[2] == ord('7'): #LEFT PRESSED
        print('Turning left...')
        (speedL,speedR) = turn(turnDirection='l',speedL=speedL,speedR=speedR)
        print(speedL,speedR,direction)

    elif command[2] == ord('8'): # RIGHT PRESSED
        print('Turning right...')
        (speedL,speedR) = turn(turnDirection='r',speedL=speedL,speedR=speedR)
        print(speedL,speedR,direction)

    else: # this may cause issues when looping
		stop()
