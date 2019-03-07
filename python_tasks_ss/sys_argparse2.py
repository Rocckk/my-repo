'''
this module is a calculator of 2 different numbers
'''

#  Create script for calculation actions: + - * /. Script should return calculated result like: 2+6=8

import sys

args = sys.argv[1:]

if args:
    try:
        if isinstance(float(args[0]), (float, int)) and isinstance(float(args[2]), (float, int)):
            if args[1] == '+':
                print str(args[0]) + ' + ' + str(args[2]) + ' = ' + str(float(args[0]) + float(args[2]))
            elif args[1] == '-':
                print str(args[0]) + ' - ' + str(args[2]) + ' = ' + str(float(args[0]) - float(args[2]))
            elif args[1] == '/':
                print str(args[0]) + ' / ' + str(args[2]) + ' = ' + str(float(args[0]) / float(args[2]))
            elif args[1] == '*':
                print str(args[0]) + ' * ' + str(args[2]) + ' = ' + str(float(args[0]) * float(args[2]))
            else:
                print 'the arithmetic operator is invalid! please choose one of the following operators as the second argument: +, -, escaped * (\\*) or  /'

    except (ValueError):
        print 'you passed non-numeric value as an argument, please pass the integer or float'
    except(ZeroDivisionError):
        print 'division by zero is not allowed'
else:
    print 'you provided no arguments!'

