from django.shortcuts import render
from django.http import HttpResponse
from . import models


# Create your views here.
def html(request):
    return render(request, 'client.html')


def get(request):
    ip = request.GET.get('ip')
    port = request.GET.get('port')
    password = request.GET.get('password')
    key = request.GET.get('key')
    result = models.get(ip, port, password, key)
    return HttpResponse(result, content_type='text/text; charset=utf-8')
