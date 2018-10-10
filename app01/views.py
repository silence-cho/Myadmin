from django.shortcuts import render,HttpResponse

# Create your views here.


def index1(request):

    return HttpResponse('index1')


def index2(request):
    return HttpResponse('index2')

def index3(request):
    return HttpResponse('index3')
