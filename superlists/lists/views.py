from django.shortcuts import render

# Create your views here.

def homePage(request):
    context = {'itemText':request.POST.get('itemText')}
    return render(request, 'lists/home.html', context)