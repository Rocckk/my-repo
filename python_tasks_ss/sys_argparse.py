'''
this module is a calculator of n numbers 
'''
# Create script for calculating actions: + - * /. Script should return calculated result like: 2+6=8.

import argparse

parser = argparse.ArgumentParser(description='this script is a calculator, which accepts 2 integers as its arguments and a string with arithmetic sings +, -, /, * which will indicate which operation must be performed with these \
                                integers.')

parser.add_argument('-a', help='the arithmetic sign which will determine the type of arithmetic operation, e.g. + for addition, etc.', required=True, metavar='sign')

parser.add_argument('-v', help='the operands of the expression (multiple)', required=True, type=(float), nargs='+', metavar=('operand1', 'operand2'))


args = parser.parse_args()



try:
    if args.a == '+':
        print sum(args.v)
    elif args.a == '-':
        print reduce(lambda x, y: x-y, args.v)
    elif args.a == '/':
        print reduce(lambda x, y: x/y, args.v)
    elif args.a == '*':
        print reduce(lambda x, y: x*y, args.v)
    else:
        print 'invalid arithmetic sign was passed as the argument -a, please choose from \'+\', \'-\', \'*\', necessarily escaped with a backslash (\), or  \'/\''
except (ZeroDivisionError):
    print 'division by zero is not allowed!'
