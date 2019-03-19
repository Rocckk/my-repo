'''
this module is a server which gives client tasks and updates database, detecting which client is free, which task is free and what is the result of the task
'''
from http.server import BaseHTTPRequestHandler
import json
from socketserver import TCPServer
import pymysql
from urllib.parse import parse_qs
from datetime import datetime
import logging
from db_handler import DBUpdater


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        '''
        this method accepts get requests from clients, checks if a client is free and gives it a task; if there are no available tasks - the server responds with status 204
        params:
        GET request objects from clients
        returns:
        None
        '''
        logging.info("the client called the server's GET method, so it's asking for task")
        # find out the unique name of the client which should be in url: it cannot be a collection
        client = parse_qs(self.path.lstrip('/?'))
        client_name = ''.join(client['name'])
        logging.info('the name of the client which requested a task is {}'.format(client_name))
        #  check if the client exists in the database, if no - he has to be inserted into it
        """
        connection = pymysql.connect(host='localhost', user='itymos', password='qSa$5cQf', db='jobs')
        cursor = connection.cursor()
        # if there are no users in db with such a name - it will be added there
        if cursor.execute('select * from `clients` where name = \'{}\''.format(client_name)) < 1:
        """
        handler = DBUpdater(client_name=client_name)
        print('$$', handler.client_name)
        if not handler.check_presence():
            logging.info("the client {} is not in a database yet".format(client_name))
            #  client is added and checks for successful addition are performed
            if handler.insert_n_client():
                logging.info("client {} was successfully added to the db".format(client_name))
                print('client was added to the db')
            else:
                logging.warning("new client {} was not successfully added to the db due to some server problem".format(client_name))
                print('client was not added to the db')
                self.send_response(500)
                self.end_headers()
                return

        """
            if cursor.execute('insert into `clients`(`name`, `status`) values(\'{}\', \'free\')'.format(client_name)):
                connection.commit()
                print('client was added to the db')
                logging.info("client {} was successfully added to the db".format(client_name))
            else:
                print('client was not added to the db')
                logging.warning("new client {} was not successfully added to the db due to some server problem".format(client_name))
                self.send_response(500)
                self.end_headers()
                connection.close()
                return
        
        #  NOT NEEDED ANYMORE, AS CLIENT CAN'T BY BUSY IF IT ASKS FOR TASK
        #  checking the status of the client, it has to be free to get the task
        cursor.execute("select `status` from `clients` where `name` = '{}'".format(client_name))
        status = cursor.fetchone()
        if status[0] == 'busy':
            print('this client is busy still')
            logging.warning('the client {} is still busy and is not allowed to take any tasks'.format(client_name))
            self.send_response(403)
            self.end_headers()
            connection.close()    
            return
        logging.info('the client {} is free and ready to take a task'.format(client_name))
        """
        #  checking for free tasks
        # if there are no available tasks - handler returns None
        try:
            task_name, task_id = handler.check_free_tasks()
            if task_name:
                logging.info('the client {} took a task {}'.format(client_name, task_name))
                #  if everything is fine: there are available tasks - update the db
                if not handler.update_all_get(task_name, task_id):
                    logging.warning('the db was not successfully updated, it remained in the previous state')
                    self.send_response(501)
                    self.end_headers()
                    return
                logging.info('the db was successfully updated')
                logging.info('the GET request from client {} was successful'.format(client_name))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(task_name.encode())
        except TypeError:
            #  if there are no available tasks - send empty response
            logging.info('all the tasks are currently busy or already done, but the GET request from client {} was successful'.format(client_name))
            self.send_response(204)
            self.end_headers()


        """
        if cursor.execute("select * frelse:
            #  if there are no available tasks - send empty response
            logging.info('all the tasks are currently busy, but the GET request from client {} was successful'.format(client_name))
            self.send_response(204)
            self.end_headers()om `tasks` where status = 'free'"):
            free_task = cursor.fetchone()
            task_id  = free_task[0]
            task_name = free_task[1]
            logging.info('the client {} took a task {}'.format(client_name, task_name))
            #  if everything is fine: client is free and there are available tasks - update the db
            if cursor.execute("update `clients` set `status` = 'busy' where `name` = '{}'".format(client_name)):
                connection.commit()
                logging.info('the client {} became busy and table \'clients\' was successfully updated'.format(client_name))
            else:
                print("table clients was not successfully updated")
                logging.warning("table `clients` was not successfully updated")
                self.send_response(501)
                self.end_headers()
                connection.close()
                return
            # check if table tasks was indeed updated:
            if cursor.execute("update `tasks` set `status` = 'taken' where `id` = '{}'".format(task_id)):
                connection.commit()
                logging.info('the task {} is now taken  and table \'tasks\' was successfully updated'.format(task_name))
            else:
                print("table 'tasks' waelse:
            #  if there are no available tasks - send empty response
            logging.info('all the tasks are currently busy, but the GET request from client {} was successful'.format(client_name))
            self.send_response(204)
            self.end_headers()s not successfully updated")
                logging.warning("table `tasks` was not successfully updated, the db is returned to the previous state")
                #  if this update failed, the client should not be busy any more too for integrity purpose
                cursor.execute("update `clients` set `status` = 'free' where `name` = '{}'".format(client_name))
                connection.commit()
                self.send_response(501)
                self.end_headers()
                connection.close()
                return
            # check if table results was indeed updated:
            if cursor.execute("insert into `results`(`task_id`, `client_id`, `start_time`) values({}, "
                              "(select `id` from clients where `name` = '{}'), '{}')".format(task_id, client_name, datetime.today().strftime('%Y-%m-%d %H:%M:%S'))):
                connection.commit()
                logging.info('the table \'results\' was successfully updated')
            else:
                print("table 'results' was not successfully updated")
                logging.warning('the table \'results\' was not successfully updated')
                #  if this update failed, the previous updates should be reversed
                cursor.execute("update `clients` set `status` = 'free' where `name` = '{}'".format(client_name))
                connection.commit()
                cursor.execute("update `tasks` set `status` = 'free' where `id` = '{}'".format(task_id))
                connection.commit()                                                      
                self.send_response(501)
                self.end_headers()
                connection.close()
                return
            #  if there are free tasks and db was updated - response and task is sent:
            logging.info('the GET request from client {} was successful'.format(client_name))
            self.send_response(200)
            self.end_headers()
            #  turn task into a string and in bytes then
            # str_task = json.dumps(task_name)
            self.wfile.write(task_name.encode())
        else:
            #  if there are no available tasks - send empty response
            logging.info('all the tasks are currently busy, but the GET request from client {} was successful'.format(client_name))
            self.send_response(204)
            self.end_headers()
        
        connection.close()
        """
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
        #  NOT NEEDED ANYMORE BECAUSE OF LACK OF OPTIONS
         
        if res:
            res = json.loads(res.decode())
            handler = DBUpdater(res=res)
            if not handler.update_all_post():
                logging.warning('the db was not successfully updated, it remained in the previous state')
                self.send_response(501)
                self.end_headers()
                return
            self.send_response(201)
            self.end_headers()
            logging.info('the db was successfully updated')
            logging.info('the POST request from client {} was successful'.format(res['client']))
            return
        print('bad result from client')



        """
        else:
            print('waiting for options from client')
            self.send_response(201)
            self.end_headers()
            return
        
        connection = pymysql.connect(host='localhost', user='itymos', password='qSa$5cQf', db='jobs')
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
            res = 'client tries to post task which it has not yet taken'
            print(res)
            reply = 'the server refuses POST request because of illegal client\'s action: ' + res
            self.send_response(403)
            self.end_headers()
            self.wfile.write(reply.encode())
            return
        """


port = 8080
if __name__ == '__main__':
    with TCPServer(('',  port), RequestHandler) as httpd:
        print('started server at port {}'.format(str(port)))
        #  actions of the server should be logged, so log file should be created or appended if it exists
        l = open('server_client.log', 'a')
        l.close()
        print('the log file \'server_client.log\' was created in append mode in current directory by server or it already exists')
        logging.basicConfig(filename='server_client.log', level=logging.INFO, format='%(asctime)s: %(levelname)s -- logged by: %(filename)s -- %(message)s')
        httpd.serve_forever()

