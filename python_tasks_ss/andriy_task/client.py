'''
this module is the HTTP client which communicates with server: asks for available tasks, processes them and returns a result to the server
'''

import requests
from datetime import datetime
import json
import subprocess as bash
from random import randint
import argparse
import pymysql
from time import sleep
import task_handler





parser = argparse.ArgumentParser(description='the script should be used with the options only if you are prompted to do that')
group = parser.add_mutually_exclusive_group()
group.add_argument('--c', help='a bash command which will be used by this script to generate new tasks', metavar='command')
group.add_argument('--f', help='choose the file to remove if appropriate task was given', metavar='file')
group.add_argument('--d', help='choose the directory to remove if appropriate task was given', metavar='dir')
group.add_argument('--r', help='create a dump of a command', nargs='+', metavar=('command', 'option'))
args = parser.parse_args()


 #  handling task
"""
def task_handler(task):
    '''
    the function handles the tasks which are received from the server and replies with the output and result
    params:
    task - a string with the name of the task which is sent by the server
    returns: 
    json with the client_name, task name, result of the task, its output and timestamp
    '''
    if task == 'uniqueness counter':
        try:
            with open('test_file.txt', 'r') as f:
                cont = f.read()
                list_content = cont.split()
                uniq_count = 0
                for i in list_content:
                    if list_content.count(i) == 1:
                        uniq_count += 1
                output = 'there are {} unique words in the file'.format(str(uniq_count))
                resp = {"client":name, "task": task, "result": "success", "output": output, 'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
        except FileNotFoundError as e:
            resp = {"client": name, "task": task, "result": "failure", "output": e.args[1],
                    'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}

    #   CHECK FOR RIGHTS TO CREATE/DELETE SHOULD BE DONE!
    elif task == 'file creator':
        proc = bash.run('touch tfile{}'.format(str(randint(0,100))), shell=True)
        #if such file exists already - try another name
        while proc.returncode != 0:
            proc = bash.run('tfile{}'.format(str(randint(0,100))), shell=True)
        output = 'a new file was created'
        print(output + ' successfully')
        resp = {"client":name, "task": task, "result": "success", "output": output, 'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
    elif task == 'directory creator':
        proc = bash.run('mkdir tdir{}'.format(str(randint(0,100))), shell=True)
        #if such dir exists already - try another name
        while proc.returncode != 0:
            proc = bash.run('mkdir tdir{}'.format(str(randint(0,100))), shell=True)
        output = 'a new dir was created'
        print(output + ' successfully')
        resp = {"client":name, "task": task, "result": "success", "output": output, 'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
    elif task == 'file deleter':
        print('please run this script again with option --f <file_to_delete> and the <file_to_delete> will be deleted')
        return
    elif task == 'dir deleter':
        print('please run this script again with option --d <direcroty_to_delete> and the <directory_to_delete> will be deleted')
        return                                                      
    elif task == 'dump maker':
        print('please run this script again with option --r <command> and provide a shell <command> (it can be with options as well) the output of which will be dumped. The command should be written in parentheses! Example:\npython client.py --r \'ls -a\'')
        return
    elif task == 'task creator':
        print('please run this client again with some simple bash command (without any options, the command must be suitable for using by itself) as its argument after \'-- c\' and new tasks will be created using this command and added to the database, e.g.:\n python client.py --c date')
        return
    return json.dumps(resp)
"""

def arg_handler():
    if args.c:
        task = 'task creator'
        comm = args.c
        proc = bash.run('{}'.format(comm), shell=True, stderr=bash.PIPE, stdout = bash.PIPE)
        #  if there was an error during program execution - it's not suitable
        if proc.stderr:
            print ('this command cannot be used without options and arguments, please choose a different command')
            res = 'failure'
            output = 'not created'
        else:
            #  if there was no error - get the info on this command and create a new task with it
            proc_data = bash.run("whatis {} | sed '2,$ d'".format(comm), shell=True, stdout=bash.PIPE)
            desc = proc_data.stdout.decode()
            #desc = re.sub(".\x08", "", proc.stdout.decode())
            #print(desc)

            stop = desc.find('(')
            new_task = 'custom '+ desc[:stop] + ' task'

            start = desc.find('- ') + 2
            end = desc.find('\n')
            description = desc[start:end]
            # print(description)
            #  inserting new task into db
            connection = pymysql.connect(host='localhost', user='root', password='2742q216', db='jobs')
            cursor = connection.cursor()
            try: 
                if cursor.execute("insert into `tasks` (`name`, `description`, `status`) values ('{}', '{}', 'free')".format(new_task, description)):
                    #  if insertion was successful
                    connection.commit()
                    print('a new task was successfully created')
                    res = 'success'
                    output = 'created'
                else:
                    print('new task was not inserted!')
                    res = 'failure'
                    output = 'not created'
            except(pymysql.err.IntegrityError):
                #  if the same command was passed as the argument and the task with same name already exists - the command should be changed
                print("the task associated with shell command '{}' already exists in the database, please try again with a different command!".format(comm))
                res = 'failure'
                output = 'not created'
            finally:
                connection.close()
                
    elif args.f:
        task = 'file deleter'
        proc = bash.run('rm {}'.format(args.f), shell=True)
        if proc.returncode != 0:
            print('file was not deleted successfully')
            output = 'a file was not deleted'
            res = 'failure'
        else:
            print('The file was deleted successfully')
            output = 'a file was deleted'
            res = 'success'
    elif args.d:
        task = 'dir deleter' 
        proc = bash.run('rmdir  {}'.format(args.d), shell=True)
        if proc.returncode != 0:
            output = 'a directory was not deleted'
            res = 'failure'
            print('dir was not deleted successfully')
        else:
            print('The dir was deleted successfully')
            output = 'a dir was deleted'
            res = 'success'
    else:
        # then arg.r
        task = 'dump maker'
        # print('**', args.r)
        # fix arguments with -, they cause error!
        proc = bash.run(args.r, shell=True, stderr=bash.STDOUT, stdout=bash.PIPE)
        output = proc.stdout.decode()
        # print(output)
        if output:
            res = "success"
            print('the dump was made successfully')
        else:
            print('the dump was not made successfully')
            res = 'failure'
    resp = json.dumps({"client":name, "task": task, "result": res, "output": output, 'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')})
    p = requests.post('http://127.0.0.1:8081', resp)
    #  if the client did the task successfully but server refuses to update the task because the client submits task with arguments (i.e. does some task without asking it from server first)
    if p.status_code == 403:
        print('but ' + p.text)



#       REDO WITH 'DONE' STATUS OF THE TASK: THIS TASK CAN'T BE DONE ANYMORE


if __name__ == "__main__":
    task_list = ['uniqueness counter', 'file creator', 'directory creator', 'file deleter', 'dir deleter', 'dump maker', 'task creator']
    #  unique name of the client, always the same, several clients with the same name are not allowed! the name cannot be a collection, only a string, int, float. 
    name = 'client_A'
    params = {"name": name}
    #  ask for task and provide client name for identification
    while True:
        try:
            r = requests.get('http://127.0.0.1:8081', params=params)
            if r.status_code == 200:
                task = r.text
                print("the task you received is {}".format(task))
                if task in task_list:
                    handler = task_handler.TaskDoer(task, name)
                    data = handler.do()
                    print('data:', data)
                else:
                    print('Unknown task')
                    data = json.dumps({"client":name, "task": task, "result": 'success', "output": 'no logic for newly created task as of now', 'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')} ) 
                p = requests.post('http://127.0.0.1:8081',  data)
            elif r.status_code == 204:
                print('no available tasks for now, please try again later')
            elif str(r.status_code).startswith('4'):
                print('client error')
            elif str(r.status_code).startswith('5'):
                print('server error occurred')
            '''
            #  if arguments were not provided to the script
            if not args.c and not args.f and  not args.d and not args.r:
                if not isinstance(params['name'], (dict, list, set, tuple)):
                    r = requests.get('http://127.0.0.1:8081', params=params)
                    #  if there are free tasks and one was received:
                    if r.status_code == 200:
                        task = r.text
                        print("the task you received is {}".format(task))
                        if task in task_list:
                            data = task_handler(task)
                            # print('data:', data)
                            p = requests.post('http://127.0.0.1:8081', data)
                        else:
                            print('Unknown task')
                            data = json.dumps({"client":name, "task": task, "result": 'success', "output": 'no logic for newly created task as of now', 'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')} ) 
                            p = requests.post('http://127.0.0.1:8081',  data)
                    elif r.status_code == 204:
                        print('no available tasks for now, please try again later')
                    elif str(r.status_code).startswith('4'):
                        print('client error')
                    elif str(r.status_code).startswith('5'):
                        print('server error occurred')
                else:
                    print('invalid client name!')

            #  if there are arguments:
            else:
                arg_handler()
            '''
             
        except requests.exceptions.ConnectionError as e:
            print(e)
            print('the server seems to be inactive or failed to reply')
        finally:
            sleep(5)





 



 
