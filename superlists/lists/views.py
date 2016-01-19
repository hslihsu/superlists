from django.shortcuts import render, redirect
from lists.models import Item
# Create your views here.


def homePage(request):
    if request.method=='POST':
        Item.objects.create(text=request.POST.get('itemText', ''))
        return redirect('/lists/the-only-list-in-the-world/')
    items = Item.objects.all()
    return render(request, 'lists/home.html', {'items':items})


def viewLists(request):
    items = Item.objects.all()
    return render(request, 'lists/home.html', {'items':items})