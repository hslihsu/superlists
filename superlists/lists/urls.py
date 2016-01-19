from django.conf.urls import url
from lists import views

 
urlpatterns = [
    url(r'^$', views.homePage, name='homePage'),
    url(r'^the-only-list-in-the-world/$', views.viewLists, name='viewLists'),
]