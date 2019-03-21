'''
this module is the HTTP client which communicates with server: asks for available tasks, sends received tasks to the task handler and when the results are received from the task handler - posts it to the server
'''

import requests
import json
from time import sleep
import logging
from task_handler import TaskDoer


if __name__ == "__main__":
    task_dict = {1:'uniqueness counter', 2: 'file creator', 3: 'directory creator', 4: 'file deleter', 5: 'dir deleter', 6: 'dump maker', 7: 'task creator'}
    logging.basicConfig(filename='server_client.log', level=logging.INFO, format='%(asctime)s: %(levelname)s -- logged by: %(filename)s -- %(message)s')
    #  ask for task
    while True:
        try:
            r = requests.get('http://127.0.0.1:8080')
            logging.info('the GET request to server has been sent')
            if r.status_code == 200:
                task = json.loads(r.text)
                print('clients received', task)
                logging.info('the client received response and got the task of type {}'. format(str(task[0])))
                handler = TaskDoer(task)
                logging.info('the client sent task to the handler')
                data = handler.do()
                print('data received from task handler:', data)
                p = requests.post('http://127.0.0.1:8080',  data)
                logging.info('the POST request has been sent to the server')
            elif r.status_code == 204:
                print('no available tasks for now')
                logging.info('no available tasks for now')
            elif str(r.status_code).startswith('4'):
                 print('client error')
                 logging.warning('invalid request has been sent to the server')
            elif str(r.status_code).startswith('5'):
                print('server error occurred')
                logging.warning('error occurred on server\'s side')
        except requests.exceptions.ConnectionError:    
            print('the server seems to be inactive or failed to reply')
            logging.warning('the client did not get any response to its request')
        finally:
            sleep(5)

  
