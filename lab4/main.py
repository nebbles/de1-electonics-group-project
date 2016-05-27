#  A welcome programme specific to the group for Lab Session 4
#  Written by: Peter Cheung  Version: 1.0  25 May 2016
import machine
import pyb

print('This is main.py')

def start():
    choice = input('Please type in the name of a script: ')

    if choice == 'task1':
        execfile('task1.py')
    elif choice == 'task2':
        execfile('task2.py')
    elif choice == 'task3':
        execfile('task3.py')
    elif choice == 'task4':
        execfile('task4.py')
    elif choice == 'task5':
        execfile('task5.py')
    elif choice == 'task6':
        execfile('task6.py')
    elif choice == 'task7':
        execfile('task7.py')
    elif choice == 'task8':
        execfile('task8.py')
    elif choice == 'task9':
        execfile('task9.py')
    else:
        print('You did not type a valid script name. Please try again.')
        start()
start()
