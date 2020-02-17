from celery import Celery

app = Celery('test', broker='pyamqp://guest@localhost//', backend='rpc://')

app.conf.broker_heartbeat = 0


@app.task
def do(x, y):
    print(str(x) + 'and ' + str(y) + 'is processed')
    return x * y

@app.task
def gen_prime(x):
    multiples = []
    results = []
    for i in range(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in range(i*i, x+1, i):
                multiples.append(j)
    return results

@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)
