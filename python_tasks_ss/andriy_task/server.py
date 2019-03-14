from http.server import BaseHTTPRequestHandler
import json
from socketserver import TCPServer
import pymysql
from urllib.parse import parse_qs
from datetime import datetime


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # find out the unique name of the client which should be in url: it cannot be a collection
        client = parse_qs(self.path.lstrip('/?'))
        if not isinstance(client, (str, int, float)):
            print('wrong name for the client')
            self.send_response(400)
            self.end_headers()
            return
        client_name = ''.join(client['name'])
        print(client_name)
        #  check if the client exists in the database, if no - he has to be inserted into it  
        connection = pymysql.connect(host='localhost', user='itymos', password='qSa$5cQf', db='jobs')
        cursor = connection.cursor()
        # if there are no users in db with such a name
        if cursor.execute('select * from `clients` where name = \'{}\''.format(client_name)) < 1:
            print('##', cursor.execute('select * from `clients` where name = \'{}\''.format(client_name)))
            cursor.execute('insert into `clients`(`name`, `status`) values(\'{}\', \'free\')'.format(client_name))
            connection.commit()
        #  checking for free tasks
        # cursor.execute("select * from `tasks` where status = 'free'")
        if cursor.execute("select * from `tasks` where status = 'free'"):
            free_task = cursor.fetchone()
            print('fre', free_task)
            task_id  = free_task[0]
            task_name = free_task[1]    
            #  if task is sent - db should be updated
            cursor.execute("update `clients` set `status` = 'busy' where `name` = '{}'".format(client_name))
            print('^', cursor.execute("update `clients` set `status` = 'busy' where `name` = '{}'".format(client_name)))
            connection.commit()
            cursor.execute("update `tasks` set `status` = 'taken' where `id` = '{}'".format(task_id))
            connection.commit()
            str_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("insert into `results`(`task_id`, `client_id`, `start_time`) values({}, (select `id` from clients where `name` = '{}'), '{}')".format(task_id, client_name, str_time))
            connection.commit()
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
        print('closed')
         
        # self.wfile.write(b"client was created!")
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
        res = json.loads(res.decode())        
        print(res)
        print(type(res))
        connection = pymysql.connect(host='localhost', user='itymos', password='qSa$5cQf', db='jobs')
        cursor = connection.cursor()
        #  updating db
        cursor.execute("update `clients` set `status` = 'free' where `name` = '{}'".format(res['client']))
        connection.commit()
        cursor.execute("update `tasks` set `status` = 'free' where `name` = '{}'".format(res['task']))
        connection.commit()
        cursor.execute("update `results` set `result` = '{}', `output` = '{}', `end_time` = '{}'".format(res['result'], res['output'], res['time']))
        connection.commit()
        self.send_response(201)
        self.end_headers()

        # self.wfile.write(result.encode())
        return


port = 8081
if __name__ == '__main__':
    with TCPServer(('',  port), RequestHandler) as httpd:
        print('started server')
        httpd.serve_forever()

