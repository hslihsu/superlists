from django.conf.urls import url
from lists import views

 
urlpatterns = [
    url(r'^$', views.homePage, name='homePage'),
]