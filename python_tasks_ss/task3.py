'''
this module accept a nested dictionary of arbitrary nested levels and arbitrary depth, parses it until all the collections are split to a non-collection (like string, integer, float, etc.)
'''

# print key information (value, type)

d = {1: 'a', 2: 'q', 3: 'e', 4: 'sfd', 5: 'sfrs'}
simple_dict={
        'points': [(0, 0), (1, 2), (4, 2)], 
        'string_key1': [{'key': 'info1', 'value': 100},{'def': ['def_file_name1', 'def_file_name2'], 'key': '/path/to/...', 'value': ['file_name_1', 'file_name_2', 'file_name_3']}, {(1, 2, 3): (1,[1, 2, 3], {'key1': {'score': 12.39}, 'key2': 100})}], 
        'string_key2': 'string_key2-value', 
        ('test', 'data'): 123654789,
        (1,2,3,7889): {2,3,67,'q', (1,2,4)}
        }

def get_dict_cont(dic, c):
    '''
    the function handles incoming data in the form of a dict, which contains unknown number of keys and values of different data types, the depth of the inside if unknown as well;
    the return value is information on every smallest possible unit of primitive data type which is not a collection (like string, int, float, etc.)
    params:
    dict - the dictionary to parse
    c - a counter which is used for formatting

    returns: the smallest possible data types from the input dict
    '''
    if isinstance(dic, dict):
        c += 1
        print '\n{}level {}'.format('\t'*c, c)
        print '{}+++++++++++++'.format('\t'*c)
        for k in dic.keys():
            if isinstance(k, tuple):
                print '{}{}'.format('\t'*c, k)
                print '{}type of {}: {}'.format('\t'*c, k, type(k))
                get_dict_cont(k, c)
            elif isinstance(k, (str, int, float)):
                print '{}{}'.format('\t'*c, k)
                print '{}type of {}: {}'.format('\t'*c, k, type(k))
        for v in dic.values():
            if isinstance(v, (str, int, float)):
                print '{}{}'.format('\t'*c, v)
                print '{}type of {}: {}'.format('\t'*c, v, type(v))
            elif isinstance(v, (tuple, list, set)):
                print '{}{}'.format('\t'*c, v)
                print '{}type of {}: {}'.format('\t'*c, v, type(v))
                get_dict_cont(v, c)
            elif isinstance(v, dict):
                print '{}{}'.format('\t'*c, v)
                print '{}type of {}: {}'.format('\t'*c, v, type(v))
                get_dict_cont(v, c)
    elif isinstance(dic, (tuple, list,set)):
        c += 1
        print '\n{}level {}'.format('\t'*c, c)
        print '{}+++++++++++++'.format('\t'*c)
        for i in dic:
            if isinstance(i, (tuple, list,set, dict)):
                print '{}{}'.format('\t'*c, i)
                print '{}type of {}: {}'.format('\t'*c, i, type(i))
                get_dict_cont(i, c)
            elif isinstance(i, (str, int, float)):
                print '{}{}'.format('\t'*c, i)
                print '{}type of {}: {}'.format('\t'*c, i, type(i))
    elif isinstance(dic, (str, int, float)):
        print '{}{}'.format('\t'*c, dic)
        print '{}type of {}: {}'.format('\t'*c, dic, type(dic))


#  the loops which enter the input dict for the first time and set counters
for k in simple_dict.keys():
    c = 0
    print '\nlevel', c
    print '+++++++++++++'
    if isinstance(k, (str, int, float)):
            print k
            print 'type of {}: {}'.format(k, type(k))
    elif isinstance(k, (tuple, list,set, dict)):
        print k
        print 'type of {}: {}'.format(k, type(k))
        get_dict_cont(k, c)
for v in simple_dict.values():
    c = 0
    print '\nlevel', c
    print '+++++++++++++'
    if isinstance(v, (str, int, float)):
            print v
            print 'type of {}: {}'.format(v, type(v))
    elif isinstance(v, (tuple, list,set, dict)):
        print v
        print 'type of {}: {}'.format(v, type(v))
        get_dict_cont(v, c)

