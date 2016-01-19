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
        
    def test_homePage_can_save_a_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['itemText'] = '新的項目'
        response = homePage(request)
        
        if response:
            response = response.content.decode('UTF-8')
        self.assertIn('新的項目', response)
        
        expectedHTML = render(request, 'lists/home.html', {'itemText':'新的項目'})
        if expectedHTML:
            expectedHTML = expectedHTML.content.decode('UTF-8')
        self.assertEqual(response, expectedHTML)