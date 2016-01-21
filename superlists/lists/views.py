from django.shortcuts import render, redirect
from lists.models import Item
# Create your views here.


def homePage(request):
    if request.method=='POST':
        Item.objects.create(text=request.POST.get('itemText', ''))
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'lists/home.html')


def viewList(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items':items})