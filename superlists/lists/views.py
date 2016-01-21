from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from lists.models import Item, List
# Create your views here.


def homePage(request):
    return render(request, 'lists/home.html')


def viewList(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items':items})

def newList(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST.get('itemText'), list=list_)
    return redirect(reverse('lists:viewList'))