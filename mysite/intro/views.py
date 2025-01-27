from django.shortcuts import render

def index(request):
    return render(request, 'intro/index.html')

def member(request):
    return render(request, 'intro/member.html')

def data_source(request):
    return render(request, 'intro/data_source.html')
