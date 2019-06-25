# from django.shortcuts import render

# Create your views here.
from .tasks import gen_num, gen_letters
from django.http import HttpResponse
from django.views import View
import time
from .models import Poll
from django.contrib.auth.models import User

class TestCelery(View):
    def get(self, request):
        print('started test1')
        print(time.perf_counter())
        res = gen_num.delay().get()
        print('result is ', res)
        print(time.perf_counter())
        print('started test2')
        print(time.perf_counter())
        res2 = gen_letters.delay().get()
        print('result2 is ', res2)
        print(time.perf_counter())
        user = User.objects.get(pk=1)
        Poll.objects.create(question='2222', created_by=user)
        return HttpResponse('done')
