#  Create decorator for wrapping data into html tags
#  decorator must be with parameters!
tag = 'b'

def decor_maker(tag):
    '''
    the function decorator which creates a true decorator
    params:
    tag - the string value which will denote an HTML tag which will wrap the value passed to a decorated function

    returns:
    decor_tag - the true function decorator
    '''
    def decor_tag(func):
        '''
        this is the genuine decorator which wraps the decorated function
        params:
        func - the decorated function

        returns:
        wrapper - the wrapper which calls the decorated function inside itself
        '''
        '''this decorated function wraps parameter 'msg' in an HTML tag passed in the parameter 'tag' as a string
        '''
        def wrapper(*args):
            '''
            the wrapper of the decorated function
            params:
            *args - the tuple of the arguments passed to the decorated function

            returns:
            None
            '''
            print '<' + tag  + '>' + str(func(*args)) + '</' + tag  + '>\n'
        return wrapper
    return decor_tag

@decor_maker(tag)
def tag_wrapper(msg):
    '''
    this function returns some text passed to it in a msg variable
    params:
    msg - a parameter of a function, any value which is to be wrapped in a tag;

    returns:
    msg - the original value which was passed to a function
    '''
    return  msg


# function calls:
tag_wrapper({1:2})

tag_wrapper(234)

tag_wrapper('abracadabra')

tag_wrapper(2.5)





#  Create decorator for text filtering (filter or change specific words)
text = 'The void elements or singleton tags in HTML are those tags that don\'t require a closing tag to be valid. These elements are usually ones that either stand alone on the page or where the end of their contents is obvious from the context of the page itself. Tags are tags 1 112 amama'

trash = 'singleton'

replace = ('page', 'new_page')


def decorator_maker(filter_value=None, change_values=None):
    '''
    the decorator function which optionally accepts 1 or 2 arguments and passes them to the real decorator
    params:
    filter_value - if 2 arguments are passed - it is a string which should be deleted from the text; if only 1 arguments is passed: if it's a string - filter_value has to be deleted from text, it's a collection(except for a dict) - the first element of the collection has to be replaced with a second element

    returns: 
    decor_filter - the true decorator
    '''
    def decor_filter(func):
        '''
        the true decorator which accepts a decorated function and passed it farther
        params:
        func - a decorated function

        returns:
        wrapper - the wrapper of the function
        '''
        def wrapper(*args):
            '''
            the wrapper function which decorates the decorated function by deleting and/or replacing elements in int input text
            params:
            *args - the parameters of the decorated function

            returns:
            None
            '''
            if filter_value and change_values and isinstance(change_values, (tuple, list, set)):
                #  if 2 parameters are passed, second one is a collection  - both deletion and replacement are performed
                #  checking if the values passed are all strings
                if not isinstance(filter_value, str) or not isinstance(filter_value[0], str) or not isinstance(filter_value[1], str):
                    print func(*args).lower().replace(str(filter_value), "\b").replace(str(change_values[0]), str(change_values[1]))
                else:
                    print func(*args).lower().replace(filter_value, "\b").replace(change_values[0], change_values[1])
            elif not change_values and not isinstance(filter_value, (tuple, list, set)):
                #  if only one parameter is passed to the decorator and it's not a collection - then it's the value to delete
                #  checking if the value passed is a string
                if not isinstance(filter_value, str):
                    print func(*args).lower().replace(str(filter_value), "\b")
                else:
                    print func(*args).lower().replace(filter_value, "\b")
            elif not change_values and isinstance(filter_value, (tuple, list, set)):
                #  if only one parameter is passed to the decorator and it's a collection - then replacement must be performed
                #  checking if the values passed in a collection are strings
                if not isinstance(filter_value[0], str) or not isinstance(filter_value[1], str):
                    print func(*args).lower().replace(str(filter_value[0]), str(filter_value[1]))
                else:
                    print func(*args).lower().replace(filter_value[0], filter_value[1])
            elif filter_value and change_values and not isinstance(change_values, (tuple, list, set)) or not isinstance(filter_value, str):
                #  if both parameters are passed, the second value is not a collection or the first value is not a string - the input is not valid
                print 'the input of the decorator is not valid!'
            else:
                print 'something is wrong with the input'
        return wrapper
    return decor_filter

@decorator_maker(trash, replace)
def filter_text(text):
    '''this function simply returns a text passed to it as the 'text' parameter;
    parameters: 
    text - a text to filter (sting); 

    returns:
    the original value passed to the function
    '''
    return text


# function calls:
filter_text(text)
