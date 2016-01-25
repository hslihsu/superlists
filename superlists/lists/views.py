from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.utils.html import escape
from lists.forms import ItemForm
# Create your views here.


def homePage(request):
    return render(request, 'lists/home.html', {'form':ItemForm()})


def viewList(request, listID):
    list_ = List.objects.get(id=listID)
    if request.method=='GET':
        return render(request, 'lists/list.html', {'list':list_, 'form':ItemForm()})
    # request.method=='POST'
    form = ItemForm(data=request.POST)
    if form.is_valid():
        form.save(forList=list_)
        return redirect(reverse('lists:viewList', args=(list_.id, )))
    return render(request, 'lists/list.html', {'list':list_, 'form':form})

def newList(request):
    if request.method=='GET':
        return render(request, 'lists/home.html', {'form':ItemForm()})
    # request.method=='POST'
    list_ = List.objects.create()
    form = ItemForm(data=request.POST)
    if form.is_valid():
        form.save(forList=list_)
        return redirect(reverse('lists:viewList', args=(list_.id, )))
    return render(request, 'lists/home.html', {'form':form})