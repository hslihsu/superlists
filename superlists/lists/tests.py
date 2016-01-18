from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.shortcuts import render
from lists.views import homePage
# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_homePage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, homePage)
        
    def test_homePage_returns_correct_HTML(self):
        request = HttpRequest()
 
        response = homePage(request)
        if response:
            response = response.content.decode('UTF-8')
            
        expectedHTML = render(request, 'lists/home.html')
        if expectedHTML:
            expectedHTML = expectedHTML.content.decode('UTF-8')
        self.assertEqual(response, expectedHTML)