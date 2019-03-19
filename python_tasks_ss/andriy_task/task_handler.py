'''
this module processes tasks received by a client from a server: it gets a task name and based on its name it's properly handled and any result (failure or success) are sent back in json format
'''


from datetime import datetime
import subprocess as bash
from random import randint
import json
from db_handler import DBUpdater


class TaskDoer:
    def __init__(self, task, name):
        self.task = task
        self.name = name
    def do(self):
        if self.task == 'uniqueness counter':
            try:
                with open('test_file.txt', 'r') as f:
                    cont = f.read()
                    list_content = cont.split()
                    uniq_count = 0
                    for i in list_content:
                        if list_content.count(i) == 1:
                            uniq_count += 1
                    output = 'there are {} unique words in the file'.format(str(uniq_count))
                    res = 'success'
            except FileNotFoundError as e:
                res = "failure"
                output = "the file to look through was not found"
        elif self.task == 'file creator':
            proc = bash.run('touch tfile{}'.format(str(randint(0, 1000))), shell=True)
            # if such file exists already - try another name
            while proc.returncode != 0:
                proc = bash.run('tfile{}'.format(str(randint(0, 1000))), shell=True)
            output = 'a new file was created'
            print(output + ' successfully')
            res = "success"
        elif self.task == 'directory creator':
            proc = bash.run('mkdir tdir{}'.format(str(randint(0, 1000))), shell=True)
            # if such dir exists already - try another name
            while proc.returncode != 0:
                proc = bash.run('mkdir tdir{}'.format(str(randint(0, 1000))), shell=True)
            output = 'a new dir was created'
            print(output + ' successfully')
            res = "success"
        elif self.task == 'file deleter':
            proc = bash.run("ls", shell=True, stdout=bash.PIPE)
            cont = proc.stdout.decode()
            list_cont = cont.split()
            for i in list_cont:
                if i.startswith('tfile'):
                    deletion = bash.run('rm {}'.format(i), shell=True)
                    if deletion.returncode != 0:
                        print('file was not deleted successfully')
                        output = 'a file was not deleted'
                        res = 'failure'
                        break
                    else:
                        print('The file was deleted successfully')
                        output = 'a file was deleted'
                        res = 'success'
                        break
            else:
                output = "no file was found for deletion"
                res = "failure"

        elif self.task == 'dir deleter':
            proc = bash.run("ls", shell=True, stdout=bash.PIPE)
            cont = proc.stdout.decode()
            list_cont = cont.split()
            for i in list_cont:
                if i.startswith('tdir'):
                    deletion = bash.run('rmdir {}'.format(i), shell=True)
                    if deletion.returncode != 0:
                        output = 'a directory was not deleted'
                        res = 'failure'
                        print('dir was not deleted successfully')
                        break
                    else:
                        print('The dir was deleted successfully')
                        output = 'a dir was deleted'
                        res = 'success'
                        break
            else:
                output = "no dir was found for deletion"
                res = "failure"
        elif self.task == 'dump maker':
            lst = bash.run('ls /bin', shell=True, stdout=bash.PIPE)
            cont = lst.stdout.decode()
            list_cont = cont.split()
            rand = randint(0, len(list_cont))
            comm = list_cont[rand]
            print('((', comm)
            proc = bash.run(comm, shell=True, stderr=bash.STDOUT, stdout=bash.PIPE)
            output = proc.stdout.decode()
            if output:
                res = "success"
                print('the dump was made successfully')
            else:
                print('the dump was not made successfully')
                res = 'failure'
        elif self.task == 'task creator':
            lst = bash.run('ls /bin', shell=True, stdout=bash.PIPE)
            cont = lst.stdout.decode()
            list_cont = cont.split()                      
            rand = randint(0, len(list_cont)-1)
            comm = list_cont[rand]
            print('&&', comm)
            comms_w_input = ['cat', 'dd', 'ed', 'getfacl', 'pax', 'red', 'tcsh', 'csh', 'sh']
            #  if the command chosen requires input
            if comm in comms_w_input:                                                                    
                while comm in comms_w_input:
                    rand = randint(0, len(list_cont))
                    comm = list_cont[rand]
            proc = bash.run(comm, shell=True, stderr=bash.STDOUT, stdout=bash.PIPE)
            #  if there was an error during program execution - it's not suitable
            if proc.returncode != 0:
                print ('this command cannot be used without options and arguments, please choose a different command')
                res = 'failure'
                output = 'not created'
            else:
                #  if there was no error - get the info on this command and create a new task with it
                proc_data = bash.run("whatis {} | sed '2,$ d'".format(comm), shell=True, stdout=bash.PIPE)
                desc = proc_data.stdout.decode()
                stop = desc.find('(')
                new_task = 'custom '+ desc[:stop] + ' task'
                start = desc.find('- ') + 2
                end = desc.find('\n')
                description = desc[start:end]
                print('***', description)
                # if the description of the task and its name are ready
                if new_task and description:
                    obj = DBUpdater(new_task, description)
                    res, output = obj.insert_n_task()

        resp = {"client": self.name, "task": self.task, "result": res, "output": output,
                'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
        print('r', resp)
             
        return json.dumps(resp)

