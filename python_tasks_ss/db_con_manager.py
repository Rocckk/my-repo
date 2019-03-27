'''
This module is context manager (as a class) for handling DB Pool connections
'''

import pymysql

class DBConnector:
    '''
    The class-context manager, which allows to open connection to a database,
    manipulate with that db and close it automatically
    '''

    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def __enter__(self):
        '''
        The enter methow which opens connection and cursor and returns cursor
        which is later instantiated and used to manipulate the db
        '''
        self.conn = pymysql.connect(host=self.host, user=self.user, password=
                                    self.password, db=self.db)
        self.cursor = self.conn.cursor()
        print('connection established')
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        The exit method which closes both connection and cursor automatically
        '''
        self.cursor.close()
        self.conn.close()
        print('connection closed')
        if exc_tb:
            return True



with DBConnector('localhost', 'itymos', 'qSa$5cQf', 'jobs') as cursor:
    match = cursor.execute('select * from tasks where id between 1 and 5')
    print('{} records from table were matched'.format(str(match)))


