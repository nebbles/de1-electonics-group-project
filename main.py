# DE-EA1.3 Electronics Group Project
# Init on 27 May 2016
# Authors: Benedict Greenberg

import machine
from pyb import *

print('''
DE-EA1.3 Electronics Group Project
Initialised on 27 May 2016
Authors:
    Benedict Greenberg
    Felix Crowther
    Grace Chin
    Fan Mo

Main.py -- Version 1.4
''')

def f(): # callback function run when switch is pressed
    global choice
    print('Interrupt occured...')
    choice = 'pilot' # sets the 'choice' to 'autodrive' for the user

sw = pyb.Switch()
sw.callback(f) # callback event if USR switch is pressed

choice = '' # declares 'choice' as initially empty
isRepeat = False

servo = Servo(3) # servo on position 3 (X3, VIN, GND)
servo.angle(-45)

bLED = Pin('X12', Pin.OUT_PP) # Blue LED // indicate recording
yLED = Pin('X11', Pin.OUT_PP) # Yellow LED // currently unused
rLED = Pin('X10', Pin.OUT_PP) # Red LED // indicate playback
led1 = pyb.LED(1)
led2 = pyb.LED(2)
led3 = pyb.LED(3)
led4 = pyb.LED(4)

def toggleLED(led):
    if led == 'r':
        if rLED.value() == 0:
            rLED.high()
        elif rLED.value() == 1:
            rLED.low()
    elif led == 'y':
        if yLED.value() == 0:
            yLED.high()
        elif yLED.value() == 1:
            yLED.low()
    elif led == 'b':
        if bLED.value() == 0:
            bLED.high()
        elif bLED.value() == 1:
            bLED.low()

def start():
    global choice
    global isRepeat

    if isRepeat == False: # if this has been run once already since startup, then skip to else
        try:
            print('To use in computer mode - press Ctrl+C')
            while True:
                if choice != '': # if callback changes 'choice' then break and run the rest of start()
                    break
        except KeyboardInterrupt: # on a computer - above code can be broken
            isRepeat = True # this code has been run once already
            choice = input('Type mode: ') # first time prompt for keyboard input
    else:
        choice = input('Type mode: ') # if the user needs to provide input again

    if choice == 'help':
        print('- Help Menu -\nHere are the options available to you:')
        print('''autodrive
        task5
        pilot
        led
        servo
        leds
        boardleds
        ''')
        start()

    elif choice == 'autodrive':
        execfile('autodrive.py')

    elif choice == 'task5':
        execfile('lab4/task5.py')

    elif choice == 'pilot':
        execfile('pilot.py')

    elif choice == 'led':
        bLED = Pin('X12', Pin.OUT_PP)
        bLED.high()

    elif choice == 'servo':
        servo = Servo(3) # servo on position 3 (X3, VIN, GND)
        while True:
            angle = int(input('Angle: '))
            servo.angle(angle) # move to user defined angle

    elif choice == 'leds':
        bLED = Pin('X12', Pin.OUT_PP)
        yLED = Pin('X11', Pin.OUT_PP)
        rLED = Pin('X10', Pin.OUT_PP)
        bLED.high()
        yLED.high()
        rLED.high()

    elif choice == 'boardleds':
        led1 = pyb.LED(1)
        led2 = pyb.LED(2)
        led3 = pyb.LED(3)
        led4 = pyb.LED(4)
        while True:
            num = int(input('Choose LED number:'))
            if num == 1:
                led1.toggle()
            elif num == 2:
                led2.toggle()
            elif num == 3:
                led3.toggle()
            elif num == 4:
                led4.toggle()
            elif num == 0:
                led1.off()
                led2.off()
                led3.off()
                led4.off()

    else:
        print('You did not type a valid mode name. Please try again, or try typing help')
        start()
start()
