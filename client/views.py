from django.shortcuts import render
from django.http import HttpResponse
from .models import Redis
from RedisClient.settings import VERSION


# Create your views here.
def html(request):
    return render(request, 'client.html', {'VERSION': VERSION})


def get(request):
    args = request.GET.get('args').split(':')
    key = request.GET.get('key')
    hash_key = request.GET.get('hash_key')
    redis = Redis(*args, key, hash_key)
    result = redis.get()
    return HttpResponse(result, content_type='text/text; charset=utf-8')
