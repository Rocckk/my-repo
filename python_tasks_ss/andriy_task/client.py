'''
This module is the HTTP client which communicates with server: asks for
available tasks, sends received tasks to the task handler and when the results
are received from the task handler - posts it to the server
'''

import json
import logging
from time import sleep
import requests
from task_handler import TaskHandler

def main():
    '''
    This function is the main function of the client: it logs client's actions,
    sends GET and POST requests to the server and gives tasks to task handler
    and db handler
    '''
    logging.basicConfig(filename='server_client.log', level=logging.INFO,
                        format='%(asctime)s: %(levelname)s -- logged by:\
                                %(filename)s -- %(message)s')
    while True:
        try:
            logging.info('the client is working and is going to ask for task')
            r = requests.get('http://127.0.0.1:8080')
            logging.info('the GET request to server has been sent and response\
 received')
            if r.status_code == 200:
                task = json.loads(r.text)
                logging.info('the client received response to its GET request')
                handler = TaskHandler(task)
                logging.info('the client sent task to the handler')
                data = handler.do()
                logging.info('task handler did the task and sent back the \
result')
                try:
                    requests.post('http://127.0.0.1:8080', data)
                    logging.info('the POST request has been sent to the \
server')
                except requests.exceptions.ConnectionError:
                    logging.error('the client did not get any response to its \
P0ST request: the server seems to be inactive or failed to reply')
                    sleep(10)
            elif r.status_code == 204:
                logging.info('no available tasks for now')
                sleep(5)
            elif r.status_code >= 400 and r.status_code < 500:
                logging.warning('invalid request has been sent to the server')
            elif r.status_code >= 500:
                logging.warning('error occurred on server\'s side')
        except requests.exceptions.ConnectionError:
            logging.error('the client did not get any response to its GET \
request: the server seems to be inactive or failed to reply')
            sleep(10)


if __name__ == "__main__":
    main()
