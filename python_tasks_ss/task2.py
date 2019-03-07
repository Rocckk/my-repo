#  sorting nested dicts and lists

# general sorting, overall
nl = [
        [1,22,5,4],
        [5,62,7,1],
        [99,10,11,2]
]

nt = (
        (234,23,222222245),
        (1,2,3),
        ('z', 'k', 'b'),
)

dil = [{2:'q', 3:'e', 1:'a'}, {1:'w', 5:'re'}, {12:'s', 1:'b'}]


print sorted(nl)

# sorting with the key (by sub-list's index 3, sub-tuple's index 2 and key 1 in nested dictionary)

print 'list with key: ', sorted(nl, key=lambda k: k[3])

print 'tuple with key: ', sorted(nt, key=lambda k: k[2])

print 'dict with key: ', sorted(dil, key=lambda k: k[1])
