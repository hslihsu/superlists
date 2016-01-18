from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.

def homePage(request):
    return HttpResponse('<!doctype html><html><head><title>待辦事項清單</title></head><body></body></html>')