from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from lists.models import Item, List
# Create your views here.


def homePage(request):
    return render(request, 'lists/home.html')


def viewList(request, listID):
    list_ = List.objects.get(id=listID)
    return render(request, 'lists/list.html', {'list':list_})


def newList(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST.get('itemText'), list=list_)
    return redirect(reverse('lists:viewList', args=(list_.id, )))


def addItem(request, listID):
    list_ = List.objects.get(id=listID)
    Item.objects.create(text=request.POST['itemText'], list=list_)
    return redirect(reverse('lists:viewList', args=(list_.id, )))