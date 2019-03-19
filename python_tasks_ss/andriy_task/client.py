'''
this module is the HTTP client which communicates with server: asks for available tasks, processes them and returns a result to the server
'''

import requests
import json
import argparse
from time import sleep
from datetime import datetime
from task_handler import TaskDoer





parser = argparse.ArgumentParser(description='the script should be used with the options only if you are prompted to do that')
group = parser.add_mutually_exclusive_group()
group.add_argument('--c', help='a bash command which will be used by this script to generate new tasks', metavar='command')
group.add_argument('--f', help='choose the file to remove if appropriate task was given', metavar='file')
group.add_argument('--d', help='choose the directory to remove if appropriate task was given', metavar='dir')
group.add_argument('--r', help='create a dump of a command', nargs='+', metavar=('command', 'option'))
args = parser.parse_args()


if __name__ == "__main__":
    task_list = ['uniqueness counter', 'file creator', 'directory creator', 'file deleter', 'dir deleter', 'dump maker', 'task creator']
    #  unique name of the client, always the same, several clients with the same name are not allowed! the name cannot be a collection, only a string, int, float. 
    name = 'client_A'
    params = {"name": name}
    #  ask for task and provide client name for identification
    while True:
        try:
            r = requests.get('http://127.0.0.1:8080', params=params)
            if r.status_code == 200:
                task = r.text
                print("the task you received is {}".format(task))
                if task in task_list:
                    handler = TaskDoer(task, name)
                    data = handler.do()
                    print('data:', data)
                else:
                    print('Unknown task')
                    data = json.dumps({"client":name, "task": task, "result": 'success', "output": 'no logic for newly created task as of now', 'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')} ) 
                p = requests.post('http://127.0.0.1:8080',  data)
            elif r.status_code == 204:
                print('no available tasks for now, please try again later')
            elif str(r.status_code).startswith('4'):
                print('client error')
            elif str(r.status_code).startswith('5'):
                print('server error occurred')
        except requests.exceptions.ConnectionError as e:
            print(e)
            print('the server seems to be inactive or failed to reply')
        finally:
            sleep(5)


