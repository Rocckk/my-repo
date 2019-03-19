'''
this module is a connector to the database
'''

import pymysql
from datetime import datetime

class DBUpdater:
    def __init__(self, new_task=None, description=None, client_name=None, res=None):
        self.task_name = new_task
        self.desc = description
        self.client_name = client_name
        self.result = res
    def insert_n_task(self):
        #  inserting new task into db
        connection = pymysql.connect(host='localhost', user='itymos', password='qSa$5cQf', db='jobs')
        cursor = connection.cursor()
        try: 
            if cursor.execute("insert into `tasks` (`name`, `description`, `status`) values ('{}', '{}', 'free')".format(self.task_name, self.desc)):
                #  if insertion was successful
                connection.commit()
                print('a new task was successfully created')
                res = 'success'
                output = 'created'
                return (res, output)
            else:
                print('new task was not inserted!')
                res = 'failure'
                output = 'not created'
        except(pymysql.err.IntegrityError):
            #  if the same command was passed as the argument and the task with same name already exists - the command should be changed
            print("the task with name '{}' already exists in the database, please try again with a different command!".format(self.task_name))
            res = 'failure'
            output = 'not created'
        finally:
            cursor.close()
            connection.close()
            return (res, output)
    def check_presence(self):
        print("##", self.client_name)
        #  check if the client exists in the database, if yes - true
        connection = pymysql.connect(host='localhost', user='itymos', password='qSa$5cQf', db='jobs')
        cursor = connection.cursor()
        if cursor.execute('select * from `clients` where name = \'{}\''.format(self.client_name)) < 1:
            cursor.close()
            connection.close()
            return False
        else:
            cursor.close()
            connection.close()
            return True
    def insert_n_client(self):
        connection = pymysql.connect(host='localhost', user='itymos', password='qSa$5cQf', db='jobs')
        cursor = connection.cursor()
        if cursor.execute('insert into `clients`(`name`, `status`) values(\'{}\', \'free\')'.format(self.client_name)):
            connection.commit()
            cursor.close()
            connection.close()
            return True
        else:
            cursor.close()
            connection.close()  
            return False
    def check_free_tasks(self):
        connection = pymysql.connect(host='localhost', user='itymos', password='qSa$5cQf', db='jobs')
        cursor = connection.cursor()
        if cursor.execute("select * from `tasks` where status = 'free'"):
            free_task = cursor.fetchone()
            task_id  = free_task[0]
            task_name = free_task[1]
            cursor.close()
            connection.close()
            return (task_name, task_id)
        else:
            cursor.close()
            connection.close()
            return
    def update_all_get(self, task_name, task_id):
        connection = pymysql.connect(host='localhost', user='itymos', password='qSa$5cQf', db='jobs')
        cursor = connection.cursor()
        if cursor.execute("update `clients` set `status` = 'busy' where `name` = '{}'".format(self.client_name)):
            if cursor.execute("update `tasks` set `status` = 'taken' where `id` = '{}'".format(task_id)):
                if cursor.execute("insert into `results`(`task_id`, `client_id`, `start_time`) values({}, (select `id` from clients where `name` = '{}'), '{}')".format(task_id, self.client_name, datetime.today().strftime('%Y-%m-%d %H:%M:%S'))):
                    connection.commit()
                    cursor.close()
                    connection.close()
                    return True
        cursor.close()
        connection.close()
        return False
    def update_all_post(self):
        connection = pymysql.connect(host='localhost', user='itymos', password='qSa$5cQf', db='jobs')
        cursor = connection.cursor()
        if cursor.execute("update `clients` set `status` = 'free' where `name` = '{}'".format(self.result['client'])):
            if cursor.execute("update `tasks` set `status` = 'done' where `name` = '{}'".format(self.result['task'])):
                if cursor.execute("update `results` set `result` = '{}', `output` = '{}', `end_time` = '{}' where `client_id` = (select `id` from `clients` where `name` ='{}') and "
                          "`task_id` = (select `id` from `tasks` where `name` = '{}') and `result` is null".format(self.result['result'], self.result['output'], self.result['time'], self.result['client'], self.result['task'])):
                    connection.commit()
                    cursor.close()
                    connection.close()
                    return True
        cursor.close()
        connection.close()
        return False
