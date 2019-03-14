'''
this module is the HTTP client which communicates with server: asks for available tasks, processes them and returns a result to the server
'''

import requests
from datetime import datetime
import json
import subprocess as bash
from random import randint


task_list = ['uniqueness counter', 'file creator', 'directory creator', 'file deleter', 'dir deleter', 'dump maker']

#  unique name of the client, always the same, several clients with the same name are not allowed!
#name = 'client_A'
name = 'clientA'

params = {"name": name}

 #  handling task
def task_handler(task):
    if task == 'uniqueness counter':
        with open('test_file.txt', 'r') as f:
            cont = f.read()
            list_content = cont.split()
            uniq_count = 0
            for i in list_content:
                if list_content.count(i) == 1:
                    uniq_count += 1
            output = 'there are {} unique words in the file'.format(str(uniq_count))
            resp = {"client":name, "task": task, "result": "success", "output": output, 'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
    elif task == 'file creator':
        proc = bash.run('touch trash/tfile{}'.format(str(randint(0,100))), shell=True)
        #if such file exists already - try another name
        while proc.returncode != 0:
            print('something wrong')
            proc = bash.run('touch trash/tfile{}'.format(str(randint(0,100))), shell=True)
        output = 'a new file was created'
        resp = {"client":name, "task": task, "result": "success", "output": output, 'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
    elif task == 'directory creator':
        proc = bash.run('mkdir trash/tdir{}'.format(str(randint(0,100))), shell=True)
        #if such dir exists already - try another name
        while proc.returncode != 0:
            print('something wrong d')
            proc = bash.run('touch trash/tdir{}'.format(str(randint(0,100))), shell=True)
        output = 'a new dir was created'
        resp = {"client":name, "task": task, "result": "success", "output": output, 'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
    elif task == 'file deleter':
        proc = bash.run('rm  trash/tfile{}'.format(str(randint(0,100))), shell=True)
        #if such file does not exist already - try another name
        while proc.returncode != 0:
            print(' wrong f name')
            proc = bash.run('rm trash/tfile{}'.format(str(randint(0,100))), shell=True)
        output = 'a file was deleted'
        resp = {"client":name, "task": task, "result": "success", "output": output, 'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
    elif task == 'dir deleter':
        proc = bash.run('rmdir  trash/tdir{}'.format(str(randint(0,100))), shell=True)
        #if such dir does not exist yet - try another name
        while proc.returncode != 0:
            print(' wrong d name')
            proc = bash.run('rmdir trash/tfile{}'.format(str(randint(0,100))), shell=True)
        output = 'a dir was deleted'
        resp = {"client":name, "task": task, "result": "success", "output": output, 'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
    elif task == 'dump maker':
        comm = 'ls -a ~'
        proc = bash.run(comm, shell=True, stdout=bash.PIPE)
        output = proc.stdout.decode()
        resp = {"client":name, "task": task, "result": "success", "output": output, 'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
    return json.dumps(resp)     



#  ask for task and provide client name for identification
try:
    r = requests.get('http://127.0.0.1:8081', params=params)
    #  if there are free tasks and one was received:
    if r.status_code == 200:
        task = r.text
        if task in task_list:
            data = task_handler(task)
            print(data)
            p = requests.post('http://127.0.0.1:8081', data)
        else:
            print('Unknown task') 

except(requests.exceptions.ConnectionError):
    print('the server seems to be inactive or failed to reply')




 



 
