'''
This module creates several classes with 3+ levels of inheritance
'''

class Ancestor:
    '''
    This class is the superclass, which has only one tool
    '''
    def __init__(self, tool):
        self.tool = tool
    def __str__(self):
        return 'I am Ancestor'
    def work(self):
        print('I work using {}'.format(self.tool))


class GrandFather(Ancestor):
    '''
    This class is the superclass's child, which has 2 tools
    ''' 
    def __init__(self, tool, tool2):
        super().__init__(tool)
        self.tool2 = tool2
    def __str__(self):
        return 'I am GrandFather'
    def work(self):
        print('I work using {} and {}'.format(self.tool, self.tool2))


class Father(GrandFather):
    '''
    This class is the GrandFather's child, which has 3 tools
    '''  
    def __init__(self, tool, tool2, tool3):
        super().__init__(tool, tool2)
        self.tool3 =  tool3
    def __str__(self):
        return 'I am Father'
    def work(self):
        print('I work using {} and {} and {}'.format(self.tool, self.tool2,
              self.tool3))

class Son(Father):
    '''
    This class is the Father's child, which has 3 tools; it is also has a
    functionality to be called like a function
    '''
    def __init__(self, tool, tool2, tool3, tool4):
        super().__init__(tool, tool2, tool3)
        self.tool4 = tool4
    def __str__(self):
        return 'I am Son'
    def __call__(self):
        return 'lots of plastic!'



class GrandSon(Son):
    '''
    This class implements property, it's setter and deleter
    '''
    def __init__(self):
        self._iq = 50

    def __str__(self):
        return 'I am GrandSon'
    
    @property
    def iq(self):
        return self._iq

    @iq.setter
    def iq(self, num):
        self._iq = num

    @iq.deleter
    def iq(self):
        self._iq = 0
        print('deletion done')






human1 = Ancestor('stone')
human1.work()
print(human1)

human2 = GrandFather('stone', 'bronze')
human2.work()

human3 = Father('stone', 'bronze', 'iron')
human3.work()

human4 = Son('stone', 'bronze', 'iron', 'plastic')
human4.work()
print(human4())

human5 = GrandSon()
print(human5())
print(human5.iq)
human5.iq = 60
print(human5.iq)
del human5.iq
print(human5.iq)
