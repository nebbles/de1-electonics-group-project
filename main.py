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

Main.py -- Version 1.3
''')

def f(): # callback function run when switch is pressed
    global choice
    print('Interrupt occured...')
    choice = 'pilot' # sets the 'choice' to 'autodrive' for the user

sw = pyb.Switch()
sw.callback(f) # callback event if USR switch is pressed

choice = '' # declares 'choice' as initially empty
isRepeat = False

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
        print('autodrive')
        print('task5')
        print('pilot')
        print('led')
        print('servo')

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
        s1 = Servo(3) # servo on position 3 (X3, VIN, GND)
        while True:
            angle = int(input('Angle: '))
            s1.angle(angle) # move to user defined angle

    else:
        print('You did not type a valid mode name. Please try again, or try typing help')
        start()
start()
