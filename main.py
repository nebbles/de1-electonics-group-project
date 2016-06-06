# DE-EA1.3 Electronics Group Project
# Init on 27 May 2016
# Authors: Benedict Greenberg
# Version: 0.2

import machine
import pyb

print('main.py Running')

def start():
    choice = input('Type mode: ')

    if choice == 'help':
        print('- Help Menu -\nHere are the options available to you:')
        print('autodrive')
        print('task5')
        print('pilot')

    elif choice == 'autodrive':
        execfile('autodrive.py')

    elif choice == 'task5':
        execfile('lab4/task5.py')

    elif choice == 'pilot':
        execfile('pilot.py')

    else:
        print('You did not type a valid mode name. Please try again, or try typing help')
        start()
start()
