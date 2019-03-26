'''
This module dumps date into file
'''


class Dumper:
    '''
    This class is the data dumper itself, which has 3 methods for recreation of
    a file, appending to a file, and the counter of occurrences of some date in
    a file
    :params
    file - a text file which is used to dump data
    '''
    file = 'test.txt'

    @classmethod
    def recreate(cls, data):
        '''
        This method accepts data, and rewrites a file with it.
        :params
        data - str or list, which is a written to a file
        '''
        if isinstance(data, str):
            with open(cls.file, 'w') as f:
                f.write(data)
        elif isinstance(data, list):
            with open(cls.file, 'w') as f:
                for i in data:
                    f.write('\n' + i)
        else:
            print('invalid input data')



    @classmethod
    def append(cls, data):
        '''
        This method accepts data, and appends it to  a file.
        :params
        data - str or list, which is a written to a file
        '''
        if isinstance(data, str):
            with open(cls.file, 'a') as f:
                f.write('\n' + data)
        elif isinstance(data, list):
            with open(cls.file, 'a') as f:
                for i in data:
                    f.write('\n' + i)
        else:
            print('invalid input data')



    @classmethod
    def combine(cls, data):
        '''
        This method accepts data, checks its uniqueness and if it is indeed
        unique - appends it to  a file.
        :params
        data - str or list, which is a written to a file
        '''
        with open(cls.file) as f:
            cont = f.read()
            if isinstance(data, str):
                if data not in cont:
                    with open(cls.file, 'a') as f:
                        f.write('\n' + data)
            elif isinstance(data, list):
                for i in data:
                    if i not in cont:
                        with open(cls.file, 'a') as f:
                            f.write('\n' + i)
    @classmethod
    def occur_count(cls, data):
        '''
        This method adds an ip, phone or url to the target file and counts how
        many times this ip (phone, url) is already written to the target file;
        :params
        data - str, an ip, url or phone which is added or list, list of ips,
        urls, phones
        '''
        try:
            f = open(cls.file)
            f.close()
        except FileNotFoundError:
            print('file not found, it will be created')
            f = open(cls.file, 'w')
            f.close()
        else:
            with open(cls.file) as f:
                cont = f.read()
                if isinstance(data, str):
                    if data in cont:
                        num = cont.count(data)
                        print('the number of occurrences of ip {} \
is {}'.format(data, str(num)))
                    with open(cls.file, 'a') as f:
                        f.write('\n' + data)
                elif isinstance(data, list):
                    for i in data:
                        if i in cont:
                            num = cont.count(i)
                            print('the number of occurrences of ip {} \
is {}'.format(i, str(num)))
                        with open(cls.file, 'a') as f:
                            f.write('\n' + i)




def main():
    '''
    The main method of the module which initializes lists of input data and 
    calls Dumper class with it
    '''
    ips = ['109.169.248.247', '46.72.177.4', '83.167.113.100', '83.167.113.100',
           '95.29.198.15', '109.184.11.34', '91.227.29.79', '90.154.66.233']
    phones = ['111-22-33', '222-33-44', '333-44-55', '444-55-66', '555-66-77', \
            '666-77-88', '777-88-99', '888-99-00']
    urls = ['example1.com', 'example2.com', 'example3.com', 'example4.com',
            'example5.com', 'example6.com', 'example7.com', 'example8.com']


    Dumper.occur_count(ips)
    Dumper.recreate(phones)
    Dumper.append(ips)
    Dumper.combine(phones)




if __name__ == '__main__':
    main()
