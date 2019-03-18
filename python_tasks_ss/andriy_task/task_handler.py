 '''
this module processes tasks received by a client from a server: it gets a task name and based on its name it's properly handled and any result (failure or success) are sent back in json format
'''

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
                resp = {"client":self.name, "task": self.task, "result": "success", "output": output, 'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
                return resp
            except FileNotFoundError as e:
                resp = {"client":self.name, "task": self.task, "result": "failure", "output": e.args[1], 'time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}   
                return res


  
