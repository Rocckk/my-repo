'''
this module is a server which responds to clients' GET and POST requests, manages them and sends HTTP responses.
it also gives tasks and updates databases using specific modules
'''
from http.server import BaseHTTPRequestHandler
import json
from socketserver import TCPServer
import logging
from db_handler import DBUpdater


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        '''
        this method accepts get requests from clients, checks if there are free tasks and gives it to client in response; if there are no available tasks
        - the server responds with status 204; the server also logs results of its actions to the log file
        params:
        GET request objects from clients
        returns:
        None
        '''
        logging.info("the server received GET request from a client")
        handler = DBUpdater()
        #  checking for free tasks
        try:
            logging.info('the server will call the task handler to get a free task')
            task_id, job_type, configs = handler.check_free_tasks()
            logging.info('the server received a valid response from the task handler')
        # if there are no available tasks - handler returns None and TypeError occurs
        except TypeError:
            #  if there are no available tasks - send empty response
            logging.info('all the tasks are currently busy or already done, but the GET request from client was successful')
            self.send_response(204)
            self.end_headers()
            return
        #  if everything is fine: there are available tasks - update the db
        logging.info('the handler is going to be called to update the db')
        if not handler.update_all_get(task_id):
            logging.warning('the db was not updated, it remained in the previous state')
            self.send_response(501)
            self.end_headers()
            logging.warning('the server has sent response 501 to a client')
            return
        logging.info('the db was successfully updated')
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps((task_id, job_type, configs)).encode())
        logging.info('the server successfully sent response to the client')
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
        resp = self.rfile.read(content_length)
        res = json.loads(resp.decode())
        logging.info('the server received the POST request from a client')
        handler = DBUpdater(res=res)
        logging.info('the server is going to call db handler to update the db')
        if not handler.update_all_post():
            logging.warning('the db was not successfully updated, it remained in the previous state')
            self.send_response(501)
            self.end_headers()
            logging.warning('the server has sent response 501 to a client')
            return
        logging.info('the db was successfully updated')
        self.send_response(201)
        self.end_headers()
        logging.info('the server successfully sent response to the client')
        return


port = 8080
if __name__ == '__main__':
    with TCPServer(('',  port), RequestHandler) as httpd:
        logging.basicConfig(filename='server_client.log', level=logging.INFO, format='%(asctime)s: %(levelname)s -- logged by: %(filename)s -- %(message)s')
        logging.info("the server started at port {}".format(port))
        #  actions of the server should be logged, so log file should be created or appended if it exists
        l = open('server_client.log', 'a')
        l.close()
        logging.info('the log file \'server_client.log\' was created in append mode in current directory by server or it already exists')
        httpd.serve_forever()

