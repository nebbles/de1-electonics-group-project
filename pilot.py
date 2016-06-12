# Pilot script to control robot via bluetooth

print('Initialising Pilot Module')
print('Version 0.1')

from pyb import Pin, ADC, Timer, UART

# Key global variables
vardirection = 'f'
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
# initialise file saving

# Timer
# Command input
# record time
# record time difference and command
# repeat

# clock = pyb.Timer(1, prescaler=, period=)
# clock.counter(0) # initialise uptime counter
isFirstCommand = True
isRecording = False
previousTime = 0
durationList = []
commandList = [] # list of commands

start = pyb.millis()

def record(command):
    global isFirstCommand
    global previousTime
    global durationList
    global commandList
    global start

    timelog = pyb.elapsed_millis(start)

    if isFirstCommand == True:
        commandList.append(command)
        previousTime = timelog
        isFirstCommand = False

    elif isFirstCommand == False:
        duration = timelog - previousTime # calculate duration since last command
        durationList.append(duration) # record time from previous command
        previousTime = timelog # update the previous time for the next command
        commandList.append(command) # record the command

def decompile():
    print('Running decoder...')
    global durationList
    global commandList

    global vardirection
    global speedL
    global speedR

    if vardirection == 'f':
        vardirection = 'b'
    elif vardirection == 'b':
        vardirection = 'f'

    repetition = 0
    for line in commandList:
        if line[0] == 'correctspeed':
            print('read correctspeed command')
            pyb.delay(durationList[repetition])
            print('undoing average speed')
            setspeed(speedL=line[1],speedR=line[2])
            print('speedL',line[1],'speedR',line[2])
            print('duration',durationList[repetition])

        elif line[0] == 'stop':
            print('stop instruction read...delaying...')
            pyb.delay(durationList[repetition])
            print('undoing stop instruction')
            # set speed in opposite direction to current
            if line[3] == 'f':
                reversedDirection = 'b'
            elif line[3] == 'b':
                reversedDirection = 'f'

            direction(direction=reversedDirection,speedL=0,speedR=0)
            setspeed(speedL=line[1],speedR=line[2])



        elif line[0] == 'setDirectionForward':
            print('undoing setDirectionForward')
            direction(direction='b',speedL=line[1],speedR=line[2])
            pyb.delay(durationList[repetition])

        elif line[0] == 'setDirectionBack':
            print('undoing setDirectionBack')
            direction(direction='f',speedL=line[1],speedR=line[2])
            pyb.delay(durationList[repetition])

        elif line[0] == 'speedUp':
            print('undoing increased speed...')
            speed(mode='dec',speedL=line[1],speedR=line[2])
            print(line[1],line[2],'duration',durationList[repetition])
            pyb.delay(durationList[repetition])

        elif line[0] == 'speedDown':
            print('undoing decreased speed')
            speed(mode='inc',speedL=line[1],speedR=line[2])
            print(line[1],line[2],'duration',durationList[repetition])
            pyb.delay(durationList[repetition])

        elif line[0] == 'turnL':
            print('undoing turn left')
            turn(turnDirection='r',speedL=line[1],speedR=line[2])
            print(line[1],line[2],'duration',durationList[repetition])
            pyb.delay(durationList[repetition])

        elif line[0] == 'turnR':
            print('undoing turn right')
            turn(turnDirection='l',speedL=line[1],speedR=line[2])
            print(line[1],line[2],'duration',durationList[repetition])
            pyb.delay(durationList[repetition])

        repetition += 1
    print('Decompile has completed')
    (vardirection,speedL,speedR) = direction(direction='f',speedL=0,speedR=0) # return to defaults
    print('Default settings returned.')
    print('Direction:',vardirection,'speedL:',speedL,'speedR:',speedR)
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

    setspeed(speedL=speedL,speedR=speedR)
    return (speedL,speedR)

def stop():
    speedL = 0
    speedR = 0
    setspeed(speedL,speedR)
    return (speedL, speedR)

def setspeed(speedL,speedR):
    	ch1.pulse_width_percent(speedR) # send a pulse of width 50% to motor1
    	ch2.pulse_width_percent(speedL) # send a pulse of width 50% to motor2

def turn(turnDirection, speedL, speedR):
    if turnDirection == 'l':
        if speedL > 4:
            speedL -= 5
        if speedR <96:
            speedR += 5

    elif turnDirection == 'r':
        if speedL <96:
            speedL += 5
        if speedR >4:
            speedR -= 5

    setspeed(speedL,speedR)
    return (speedL,speedR)

def correctspeed(speedL,speedR):
    average = (speedL + speedR)/2
    if average % 5 != 0:
        average += 2.5
    speedL = int(average)
    speedR = int(average)
    setspeed(speedL,speedR)
    return (speedL,speedR)

# loop
# Use keypad controller to control car
print(vardirection,speedL,speedR)

direction(direction=vardirection,speedL=speedL,speedR=speedR) # call to set motor direction

while True:				# loop forever until CTRL-C
    while (uart.any()!=10):    #wait we get 10 chars
        n = uart.any()
    command = uart.read(10)
    if command[2] == ord('1'): # record
        print('Recording has been toggled.')
        if isRecording == False and speedL == 0 and speedR == 0:
            isRecording = True

            durationList = [] # wipe list
            commandList = [] # wipe list
            print('Journey memory wiped.')
            print('Recording enabled.')
        elif isRecording == True:
            timelog = pyb.elapsed_millis(start)
            duration = timelog - previousTime
            durationList.append(duration) # record time from previous command
            isRecording = False

            print(commandList)
            print(durationList)

            durationList.reverse()
            commandList.reverse()

            print(commandList)
            print(durationList)

            print('Recording disabled')

    elif command[2] == ord('2'): # play
        print('Command not available yet')
        if isRecording == True:
            pass
        elif isRecording == False and speedL == 0 and speedR == 0:
            print('Retracing route...')
            decompile() # run decompiler

    elif command[2] == ord('3'): # straigten travel direction
        record(['correctspeed',speedL,speedR])
        print('Correcting motor speeds...')
        (speedL,speedR) = correctspeed(speedL,speedR)

    elif command[2] == ord('4'): # emergency stop / change direction
        print('Stopping...or changing direction...')
        if speedL==0 and speedR==0:
            # change direction
            print('Changing direction...')
            if vardirection == 'f':
                record(['setDirectionBack',speedL,speedR])
                (vardirection,speedL,speedR) = direction(direction='b',speedL=speedL,speedR=speedR)
                print('SpeedL=',speedL,'SpeedR=',speedR,'Direction=',vardirection)
            elif vardirection == 'b':
                record(['setDirectionForward',speedL,speedR])
                (vardirection,speedL,speedR) = direction(direction='f',speedL=speedL,speedR=speedR)
                print('SpeedL=',speedL,'SpeedR=',speedR,'Direction=',vardirection)
        else:
            record(['stop',speedL,speedR,vardirection])
            print('Stopping...')
            (speedL,speedR) = stop()
        print(speedL,speedR)

    elif command[2] == ord('5'): # UP pressed
        print('Increasing speed...')
        (speedL,speedR) = speed(mode='inc',speedL=speedL,speedR=speedR)
        print(speedL,speedR,vardirection)
        record(['speedUp',speedL,speedR])

    elif command[2] == ord('6'): # DOWN PRESSED
        print('Decreasing speed...')
        (speedL,speedR) = speed(mode='dec',speedL=speedL,speedR=speedR)
        print(speedL,speedR,vardirection)
        record(['speedDown',speedL,speedR])

    elif command[2] == ord('7'): #LEFT PRESSED
        print('Turning left...')
        (speedL,speedR) = turn(turnDirection='l',speedL=speedL,speedR=speedR)
        print(speedL,speedR,vardirection)
        record(['turnL',speedL,speedR])


    elif command[2] == ord('8'): # RIGHT PRESSED
        print('Turning right...')
        (speedL,speedR) = turn(turnDirection='r',speedL=speedL,speedR=speedR)
        print(speedL,speedR,vardirection)
        record(['turnR',speedL,speedR])

    else: # writing to the robot with UART
        message = 'command not understood'
        print(message)
        print(command)
        for i in range(22):
    		uart.writechar(ord(message[i]))
    	uart.writechar(13)
    	uart.writechar(10)
