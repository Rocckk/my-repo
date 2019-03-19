'''
this module is a server which gives client tasks and updates database, detecting which client is free, which task is free and what is the result of the task
'''
from http.server import BaseHTTPRequestHandler
import json
from socketserver import TCPServer
from urllib.parse import parse_qs
import logging
from db_handler import DBUpdater


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        '''
        this method accepts get requests from clients, checks if a client is free and gives it a task; if there are no available tasks
        - the server responds with status 204; the server also logs results of its actions to the log file
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
        handler = DBUpdater(client_name=client_name)
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

