from celery import shared_task
import string
import random

@shared_task
def gen_num():
    return list(range(1, 1000, 3))

@shared_task
def gen_letters():
    return [[random.choice(string.ascii_letters) * i] for i in range(30)]