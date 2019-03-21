'''
this module is a connector to the database which updates it whenever necessary
'''

import pymysql
from datetime import datetime

class DBUpdater:
    '''
    this class is the database updater which responds to requests from clients/server to update info in db tables and fulfils them
    '''
    def __init__(self, list_of_tasks=None, res =None):
        '''
        the constructor which initializes necessary class attributes
        '''
        self.list_of_tasks = list_of_tasks
        self.result = res
    def open_conn(self):
        '''
        this method opens connection to the db and initializes cursor object to communicate with it
        :returns
        tuple: cursor - obj, the object for communicating with db; connection - the connection object
        '''
        connection = pymysql.connect(host='localhost', user='itymos', password='qSa$5cQf', db='jobs')
        cursor = connection.cursor()
        return (connection, cursor)

    def insert_n_task(self):
        '''
        the method which inserts new tasks in table `tasks`
        :params
        :returns
        res - the string with result of insertion
        output - the string with output of insertion
        '''
         
        #  inserting new task into db
        conn, cursor = self.open_conn()
        for i in self.list_of_tasks:
            if cursor.execute("insert into `tasks` (`job_type`, `config`, `created`, `status`) values ({}, '{}', '{}', 'new')".format(str(i[0]), i[1], i[2])):
                conn.commit()
            else:
                res = 'failure'
                output = 'not created'
                return (res, output)
                break
        res = 'success'
        output = 'created'
        cursor.close()
        conn.close()
        return (res, output)

    def check_free_tasks(self):
        '''
         this method checks which task is currently free and returns its id(int), job type(str) and configs(str)
        :returns
        tuple with task_id - the id of that task if there are free tasks, job_type - the type of job which this task represents and configs - the string or additional parameters needed for the task
        None - if there are no free tasks
        '''
        conn, cursor = self.open_conn()
        if cursor.execute("select * from `tasks` where status = 'new' order by 'created'"):
            free_task = cursor.fetchone()
            task_id = free_task[0]
            configs  = free_task[1]
            job_type = free_task[6]
            cursor.close()
            conn.close()
            return (task_id, job_type, configs)
        else:
            cursor.close()
            conn.close()
            return
    
    def update_all_get(self, task_id):
        '''
        this method updates the db table `tasks` for GET requests and makes sure that the changes to the db will be committed only in case when the table is indeed updated
        : params
        task_id - int, the id of the task which was sent to the client
        :returns
         True if all the table was successfully updated
        False if otherwise
        '''
        conn, cursor = self.open_conn()     
        if cursor.execute("update `tasks` set `status` = 'in progress' where id = {}".format(str(task_id))):
            conn.commit()
            cursor.close()
            conn.close()
            return True
        cursor.close()
        conn.close()
        return False
    
    def update_all_post(self):
        '''
        this method updates the db table `tasks` for POST requests and makes sure that the changes to the db will be committed only in case when the table is indeed updated
        : params
        self.result - dict, the response received from the client with results of the task
        :returns
        True if the table was successfully updated
        False if otherwise
        '''
        conn, cursor = self.open_conn()
        if self.result['result'] == 'success':
            if cursor.execute("update `tasks` set `status` = 'done', `modified` = '{}', `output` = \"{}\" where `id` = {}".format(self.result['modified'], self.result['output'], str(self.result['task_id']))):
                conn.commit()
                cursor.close()
                conn.close()
                return True
        elif self.result['result'] == 'failure': 
            if cursor.execute("update `tasks` set `status` = 'error', `modified` = '{}', `output` = \"{}\" where `id` = {}".format(self.result['modified'], self.result['output'], str(self.result['task_id']))):
                conn.commit()
                cursor.close()
                conn.close()
                return True   
        cursor.close()
        conn.close()
        return False
