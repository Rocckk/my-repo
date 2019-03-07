#  Create test script for catching different types of exceptions: should be at least 3 types of errors with correct handling

def error_tester():
    print 'the following code will be tested:\n'
    print '''l = range(10)
            for i in l:
                print l[20]'''
    try:
        l = range(10)
        for i in l:
            print l[20]

    except (IndexError):
        print 'there is no such index in the list!\n'

    print 'the following code will be tested:\n'
    print 'print l - 10'
    try:
        print l - 10

    except (TypeError):
        print 'integer can\'t be subtracted from a list!\n'

    print 'the following code will be tested:'
    print '''a = 1
print a + b'''
    try:
        a = 1
        print a + b

    except (NameError):
        print 'you did not declare a variable \'b\', declare it as an integer or float!\n'

    print 'the following code will be tested:'

    print '''import math
print math.digit'''

    try:
        import math
        print math.digit

    except (AttributeError) as a:
        print 'this module does not have the attribute \'digit\'!\n'


#  function call
error_tester()





#  user-defined exception

class MyError(Exception):
    def __init__(self, err_message):
        self.err_message = err_message

    def __str__(self):
        return self.err_message

def func(inp):
    print 'test\n'
    print inp
    try:
        if not isinstance(inp, int):
            raise MyError('only integers can be the input of this function!')
    except (MyError) as me:
        print me
        print 'an error created by me was caught and handled!'
    print 'done!'

func('abracadabra')




