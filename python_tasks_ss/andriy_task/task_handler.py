'''
this module processes tasks received by a client from a server: it gets a task name and based on its name it's properly handled and any result (failure or success) are sent back in json format
'''


from datetime import datetime
import subprocess as bash
from random import randint
import json
from db_handler import DBUpdater


class TaskDoer:
    '''
    this class is the handler of various tasks received by clients; it checks the name of the task choose the logic for its proper handling
    '''
    def __init__(self, task):
        '''
        the constructor of objects of this class
        '''
        self.task = task
    def do(self):
        '''
        this method if the universal handler of predefined tasks: depending on the task name it processes it properly
        :params
        self.task - list, the id, type of job and its gonfigs  which are passed to the method
        :returns
        resp - json-endoded dict, with the client name, task name, task result, task output and the time when the task was done  
        '''
        if self.task[1] == 1:
            try:
                 with open(self.task[2], 'r') as f:
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
        elif self.task[1] == 2:
            proc = bash.run('touch {}'.format(self.task[2]), shell=True)
            if proc.returncode != 0:
                output = 'a new file was not created'
                res = "failure"
            else:
                output = 'a new file was created'
                res = "success"
        elif self.task[1] == 3:
            proc = bash.run('mkdir {}'.format(self.task[2]), shell=True)
            if proc.returncode != 0:
                output = 'a new dir was not created'
                res = "failure"
            else:
                output = 'a new dir was created'
                res = "success"
        elif self.task[1] == 4:
            deletion = bash.run('rm {}'.format(self.task[2]), shell=True)
            if deletion.returncode != 0:
                output = 'a file was not deleted'
                res = 'failure'
            else:
                output = 'a file was deleted'
                res = 'success'
        elif self.task[1] == 5:
            deletion = bash.run('rmdir {}'.format(self.task[2]), shell=True)
            if deletion.returncode != 0:
                output = 'a directory was not deleted'
                res = 'failure'
            else:
                output = 'a dir was deleted'
                res = 'success'
        elif self.task[1] == 6:
            try:
                proc = bash.run(self.task[2], shell=True, stderr=bash.STDOUT, stdout=bash.PIPE, timeout=3)
                output = proc.stdout.decode()
                if output:
                    res = "success"
                else:
                    res = 'failure'
            except bash.TimeoutExpired:
                output = 'no output, command timed out returning nothing'
                res = 'failure' 
        elif self.task[1] == 7:
            conf = int(self.task[2])
            file_path_list = ["/home/itymos/git_thing/my-repo/python_tasks_ss/andriy_task/test_dir/a.txt",
                        "/home/itymos/git_thing/my-repo/python_tasks_ss/andriy_task/test_dir/b.txt",
                        "/home/itymos/git_thing/my-repo/python_tasks_ss/andriy_task/test_dir/c.txt "
                        ]
            dir_path_list = ["/home/itymos/git_thing/my-repo/python_tasks_ss/andriy_task/test_dir/a_dir",
                        "/home/itymos/git_thing/my-repo/python_tasks_ss/andriy_task/test_dir/b_dir",
                        "/home/itymos/git_thing/my-repo/python_tasks_ss/andriy_task/test_dir/c_dir"
                        ]
            list_of_tasks = []
            for i in range(conf):
                task = []
                j_type = randint(1,7)
                task.append(j_type)
                if j_type in [1, 2, 4]:
                    task_conf = file_path_list[randint(0, len(file_path_list)-1)]
                    task.append(task_conf)
                elif j_type in [3, 5]:
                    task_conf = dir_path_list[randint(0, len(file_path_list)-1)]
                    task.append(task_conf)
                elif j_type == 6:
                    lst = bash.run('ls /bin', shell=True, stdout=bash.PIPE)
                    cont = lst.stdout.decode()
                    list_cont = cont.split()                      
                    rand = randint(0, len(list_cont)-1)
                    comm = list_cont[rand]
                    comms_w_input = ['cat', 'dd', 'ed', 'getfacl', 'pax', 'red', 'tcsh', 'csh', 'sh']
                    #  if the command chosen requires input
                    if comm in comms_w_input:                                                                    
                        while comm in comms_w_input:
                            rand = randint(0, len(list_cont))
                            comm = list_cont[rand]
                    task_conf = comm
                    task.append(task_conf)
                elif j_type == 7:
                    task_conf = randint(1,4)
                    task.append(task_conf)
                task.append(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                list_of_tasks.append(task)
            #  updating db
            obj = DBUpdater(list_of_tasks)
            res, output = obj.insert_n_task()
        resp = {"task_id": self.task[0], "result": res, "output": output, 'modified': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
        return json.dumps(resp)



