'''
this module is a server which gives client tasks and updates database, detecting which client is free, which task is free and what is the result of the task
'''
from http.server import BaseHTTPRequestHandler
import json
from socketserver import TCPServer
import pymysql
from urllib.parse import parse_qs
from datetime import datetime


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        '''
        this method accepts get requests from clients, checks if a client is free and gives it a task; if there are no available tasks - the server responds with status 204
        params:
        GET request objects from clients
        returns:
        None
        '''
        # find out the unique name of the client which should be in url: it cannot be a collection
        client = parse_qs(self.path.lstrip('/?'))
        client_name = ''.join(client['name'])
        print(client_name)
        #  check if the client exists in the database, if no - he has to be inserted into it  
        connection = pymysql.connect(host='localhost', user='root', password='2742q216', db='jobs')
        cursor = connection.cursor()
        # if there are no users in db with such a name - it will be added there
        if cursor.execute('select * from `clients` where name = \'{}\''.format(client_name)) < 1:
            cursor.execute('insert into `clients`(`name`, `status`) values(\'{}\', \'free\')'.format(client_name))
            connection.commit()

        # # FIXXXX REQUIRED! IF THERE ARE NO AVAILABLE TASKS - NO NEED TO MAKE HIM BUSY; updating clients: if client ask for the task - it should receive it and become busy
        if cursor.execute(
                "update `clients` set `status` = 'busy' where `name` = '{}'".format(client_name)):
            connection.commit()
        #  if table was not updated, check if client is not yet busy :
        elif cursor.execute(
                "select `status` from `clients` where `name` = '{}'".format(client_name)):
            status = cursor.fetchone()
            if status[0] == 'busy':
                print('this client is busy still')
                self.send_response(403)
                self.end_headers()
                return
        else:
            print("table clients was not successfully updated")
            self.send_response(501)
            self.end_headers()
            return

        #  checking for free tasks
        if cursor.execute("select * from `tasks` where status = 'free'"):
            free_task = cursor.fetchone()
            print('free', free_task)
            task_id  = free_task[0]
            task_name = free_task[1]
            # check if table tasks was indeed updated:
            if cursor.execute("update `tasks` set `status` = 'taken' where `id` = '{}'".format(task_id)):
                connection.commit()
            else:
                print("table 'tasks' was not successfully updated")
                self.send_response(501)
                self.end_headers()
                return
            str_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            # check if table results was indeed updated:
            if cursor.execute("insert into `results`(`task_id`, `client_id`, `start_time`) values({}, "
                              "(select `id` from clients where `name` = '{}'), '{}')".format(task_id, client_name, str_time)):
                connection.commit()
            else:
                print("table 'results' was not successfully updated")
                self.send_response(501)
                self.end_headers()
                return
            #  if there are free tasks and db was updated - response and task is sent:
            self.send_response(200)
            self.end_headers()
            #  turn task into a string and in bytes then
            str_task = json.dumps(task_name)
            self.wfile.write(task_name.encode())
        else:
            #  if there are no available tasks - send empty response
            self.send_response(204)
            self.end_headers()
        connection.close()
        return

    def do_POST(self):
        '''
        this method handles POST requests from clients; here the results and outputs of clients' tasks are processed
        params:
        POST request objects from clients
        returns:
        None
        '''
        content_length = int(self.headers['Content-Length'])
        res = self.rfile.read(content_length)
        #  if an object was sent, not None (if clients sends None - it means some additional options are required to process the taks
        #  successfully)
        print('res', res)
        if res:
            res = json.loads(res.decode())
        else:
            print('waiting for options from client')
            self.send_response(201)
            self.end_headers()
            return
        connection = pymysql.connect(host='localhost', user='root', password='2742q216', db='jobs')
        cursor = connection.cursor()
        #  updating db
        #  here we have to make sure that a client does not post with options without sending get request first:
        #  i.e we have to check if that client already has records in `results` table with the same task_id but that record lacks result
        if cursor.execute("select * from `results` where `client_id` = (select `id` from `clients` where `name` ='{}') and "
                          "`task_id` = (select `id` from `tasks` where `name` = '{}') and `result` is null".format(res['client'], res['task'])):
            # if a client has already got some task and posts results
            if cursor.execute("update `clients` set `status` = 'free' where `name` = '{}'".format(res['client'])):
                connection.commit()
            else:
                print("table 'clients' was not successfully updated")
                self.send_response(501)
                self.end_headers()
                return
            if cursor.execute("update `tasks` set `status` = 'free' where `name` = '{}'".format(res['task'])):
                connection.commit()
            else:
                print("table 'tasks' was not successfully updated")
                self.send_response(501)
                self.end_headers()
                return
            if cursor.execute("update `results` set `result` = '{}', `output` = '{}', `end_time` = '{}' where "
                              "`client_id` = (select `id` from `clients` where `name` ='{}') and "
                          "`task_id` = (select `id` from `tasks` where `name` = '{}') and `result` "
                              "is null".format(res['result'], res['output'], res['time'], res['client'], res['task'])):
                connection.commit()
            else:
                print("table 'results' was not successfully updated")
                self.send_response(501)
                self.end_headers()
                return
            self.send_response(201)
            self.end_headers()
            # self.wfile.write(result.encode())
            return
        else:
            print('client tries to post task which it has not yet taken')
            self.send_response(403)
            self.end_headers()
            return


port = 8081
if __name__ == '__main__':
    with TCPServer(('',  port), RequestHandler) as httpd:
        print('started server')
        httpd.serve_forever()

