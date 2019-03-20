'''
this module is a connector to the database which updates it whenever necessary
'''

import pymysql
from datetime import datetime

class DBUpdater:
    '''
    this class is the database updater which responds to requests from clients/server to update info in db tables and fulfils them
    '''
    def __init__(self, new_task=None, description=None, client_name=None, res=None):
        '''
        the constructor which initializes necessary class attributes
        '''
        self.task_name = new_task
        self.desc = description
        self.client_name = client_name
        self.result = res
    def open_conn(self):
        '''
        this method opens connection to the db and initializes cursor object to communicate with it
        :returns
        tuple: cursor - obj, the object for communicating with db; connection - the connection object
        '''
        connection = pymysql.connect(host='localhost', user='root', password='2742q216', db='jobs')
        cursor = connection.cursor()
        return (connection, cursor)
    def insert_n_task(self):
        '''
        the method which inserts new tasks in table `tasks`
        :params
        self.task_name - the name of the new task (str)
        self.desc - the description of the new task (str)
        :returns
        res - the string with result of insertion
        output - the string with output of insertion
        '''
        #  inserting new task into db
        conn, cursor = self.open_conn()
        try: 
            if cursor.execute("insert into `tasks` (`name`, `description`, `status`) values ('{}', '{}', 'free')".format(self.task_name, self.desc)):
                #  if insertion was successful
                conn.commit()
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
            conn.close()
            return (res, output)
    """
    def check_presence(self):
        '''
        this method checks if the client which sends request for task is already in db
        :params
        self.client_name - str, the name of the client who sends the request
        :returns
        True - if client exists
        False - if not
        '''
        #  check if the client exists in the database, if yes - true
        conn, cursor = self.open_conn()
        if cursor.execute('select * from `clients` where name = \'{}\''.format(self.client_name)) < 1:
            cursor.close()
            conn.close()
            return False
        else:
            cursor.close()
            conn.close()
            return True
    def insert_n_client(self):
        '''
        this method inserts new client in table `clients`
        :params
        self.client_name - str, the name of the client who sends the request
        :returns:
        True if client was successfully inserter
        False if otherwise
        '''
        conn, cursor = self.open_conn()
        if cursor.execute('insert into `clients`(`name`, `status`) values(\'{}\', \'free\')'.format(self.client_name)):
            conn.commit()
            cursor.close()
            conn.close()
            return True
        else:
            cursor.close()
            conn.close()  
            return False
    """
    def check_free_tasks(self):
        '''
        this method checks which task is currently free and returns its name and id
        :returns
        tuple with task_name - the name of the free task and task_id - the id of that task if there are free tasks
        None - if there are no free tasks
        '''
        conn, cursor = self.open_conn()
        if cursor.execute("select * from `tasks` where status = 'new'"):
            free_task = cursor.fetchone()
            task_id = free_task[0]
            configs  = free_task[2]
            job_type = free_task[1]
            cursor.close()
            conn.close()
            return (task_id, job_type, configs)
        else:
            cursor.close()
            conn.close()
            return
    def update_all_get(self, task_id):
        '''
        this method updates the db tables `clients`, `tasks` and `results` for GET requests and makes sure that the changes to the db will be committed only in case when all 3 tables are updated
        : params
        self.client_name - str, the name of the client who sends the request
        task_id - int, the id of the task which was sent to the client
        :returns
        True if all the tables were successfully updated
        False if otherwise
        '''
        conn, cursor = self.open_conn()
        """
        if cursor.execute("update `clients` set `status` = 'busy' where `name` = '{}'".format(self.client_name)):
            if cursor.execute("update `tasks` set `status` = 'taken' where `id` = '{}'".format(task_id)):
                if cursor.execute("insert into `results`(`task_id`, `client_id`, `start_time`) values({}, (select `id` from clients where `name` = '{}'), '{}')".format(task_id, self.client_name, datetime.today().strftime('%Y-%m-%d %H:%M:%S'))):
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return True
        """
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
        this method updates the db tables `clients`, `tasks` and `results` for POST requests and makes sure that the changes to the db will be committed only in case when all 3 tables are updated
        : params
        self.result - dict, the response received from the client with results of the task
        :returns
        True if all the tables were successfully updated
        False if otherwise
        '''
        conn, cursor = self.open_conn()
        if cursor.execute("update `clients` set `status` = 'free' where `name` = '{}'".format(self.result['client'])):
            if cursor.execute("update `tasks` set `status` = 'done' where `name` = '{}'".format(self.result['task'])):
                if cursor.execute("update `results` set `result` = '{}', `output` = \"{}\", `end_time` = '{}' where `client_id` = (select `id` from `clients` where `name` ='{}') and "
                          "`task_id` = (select `id` from `tasks` where `name` = '{}') and `result` is null".format(self.result['result'], self.result['output'], self.result['time'], self.result['client'], self.result['task'])):
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return True
        cursor.close()
        conn.close()
        return False
