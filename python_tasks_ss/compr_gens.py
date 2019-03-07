#  input: data(list), chunk_size

#  floats should be handled

l = xrange(1,110)

l2 = ['qwer', 'asdf', 'zxcv', 'wertyy', 'dgfh', 'xcvbn', 'ert', 'fgh', 'cvbn']

def chunk_sizer(lis, size):
    '''the function which accepts a list and cuts it in chunks the size of which is specified by 'size' parameter
    params:
    lis - a list
    size - the size of a chunk

    returns:
    the chunks of list written separately
    '''
    if not isinstance(size, int):
        print 'the second parameter should be an integer!'
        return
    addend = size 
    for i in xrange(0,len(lis), size):
        yield list(lis)[i:size]
        size += addend
        if size > len(l):
            size = len(l)

g = chunk_sizer(l, 3)

g2 = chunk_sizer(l2, 4) 
for i in g:
    print i

for i in g2:
    print i



# input: start_point, end_point, step

def chunk_maker(st, stop, step):
    '''the function which creates a list from its input parameters and st and stop and cuts it into chunks the size of which is specified by step parameter
    params:
    st - start of list 
    stop - end of list                                                       :
    step - the size of chunks

    returns:
    chunks of the list
    '''
    if not isinstance(st, int) or not isinstance(stop, int) or not isinstance(step, int):
        print 'all the parameters should be integers!'
        return
    lis = range(st,stop)
    addend = step
    for i in xrange(0,len(lis), step):
        yield lis[i:step]
        step += addend
        if step > len(lis):
            step = len(lis)

g = chunk_maker(12, 275, 7.5)

g2 = chunk_maker(123, 387, 10)

for i in g:
    print i

for i in g2:
    print i
