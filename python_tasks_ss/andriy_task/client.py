'''
this module is the HTTP client which communicates with server: asks for available tasks, sends received tasks to the task handler and when the results are received from the task handler - posts it to the server
'''

import requests
import json
from time import sleep
import logging
from task_handler import TaskDoer


if __name__ == "__main__":
    logging.basicConfig(filename='server_client.log', level=logging.INFO, format='%(asctime)s: %(levelname)s -- logged by: %(filename)s -- %(message)s')
    while True:
        try:
            logging.info('the client is working and is going to ask for task')
            logging.info('the GET request to server has been sent')
            r = requests.get('http://127.0.0.1:8080')
        except requests.exceptions.ConnectionError:
            logging.error('the client did not get any response to its GET request: the server seems to be inactive or failed to reply')
        if r.status_code == 200:
            task = json.loads(r.text)
            logging.info('the client received response to its GET request')
            handler = TaskDoer(task)
            logging.info('the client sent task to the handler')
            data = handler.do()
            logging.info('task handler did the task and sent back the result')
            try:
                logging.info('the POST request has been sent to the server')
                p = requests.post('http://127.0.0.1:8080',  data)
            except requests.exceptions.ConnectionError:
                logging.error('the client did not get any response to its P0ST request: the server seems to be inactive or failed to reply')
        elif r.status_code == 204:
                logging.info('no available tasks for now')
                sleep(5)
        elif str(r.status_code).startswith('4'):
            logging.warning('invalid request has been sent to the server')
        elif str(r.status_code).startswith('5'):
            logging.warning('error occurred on server\'s side')

