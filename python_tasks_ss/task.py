import sys

#  create variables of different types: list/tuple/dict/set
l = [1,2,3,4]
t = (1,2,3,4)
s = set((1,2,3,4))
d = {1:'a', 2:'b', 3:'c', 4:'d'}
print type (l)
print type (t)
print type (s)
print type (d)

#  iterate by this data using as many possible ways as you know
# for list
for i in l:
    print i

for i, n in enumerate(l):
    print i, n

stop = len(l)
start = 0
while start < stop:
    print l[start]
    start +=1

def gen(itr):
    for i in itr:
        yield i
test = gen(l)
for i in test:
    print i 


# for tuple
for i in t:
    print i

for i, n in enumerate(t):
     print i, n

stop = len(t)
start = 0
while start < stop:
    print l[start]
    start +=1

def gen(itr):
    for i in itr:
        yield i
test = gen(t)
for i in test:
    print i


#  for dict
for k, v in d.items():
    print k, v

for k, v in enumerate(d.values()):
    print k, v

stop = len(d)
start = 0
list_of_keys = d.keys()
while start < stop:
    print d[list_of_keys[start]]
    start +=1

def gen(itr):
    for i in itr:
        yield i
test = gen(d)
for i in test:
    print i


#  for set
for i in s:
    print i

for i, n in enumerate(s):
    print n

it = iter(s)
for i in xrange(len(s)):
    print it.next()

def gen(itr):
    for i in itr:
        yield i
test = gen(s)
for i in test:
    print i
