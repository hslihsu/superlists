from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.shortcuts import render
from lists.views import homePage
from lists.models import Item
# Create your tests here.

class HomePageTest(TestCase):


    def test_root_url_resolves_to_homePage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, homePage)
        
        
    def test_homePage_can_save_a_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['itemText'] = '新的項目'
        homePage(request)
              
        self.assertEqual(Item.objects.count(), 1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, '新的項目')
        
    def test_home_page_redirect_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['itemText'] = '新的項目'
        response = homePage(request)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
        
    def test_homePage_display_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        
        request = HttpRequest()
        response = homePage(request)
        if response:
            response = response.content.decode('UTF-8')
        
        self.assertIn('itemey 1', response)
        self.assertIn('itemey 2', response)
        
    def test_homePage_only_saves_items_when_necessary(self):
        request = HttpRequest()
        homePage(request)
        self.assertEqual(Item.objects.count(), 0)
        
        
class ItemModelTest(TestCase):
    
    
    def test_saving_and_retrieving_items(self):
        firstItem = Item()
        firstItem.text = '第一個清單項目'
        firstItem.save()
        
        secondItem = Item()
        secondItem.text = '第二個清單項目'
        secondItem.save()
        
        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(), 2)
        
        firstSavedItem = savedItems[0]
        secondSavedItem = savedItems[1]
        self.assertEqual(firstSavedItem.text, '第一個清單項目')
        self.assertEqual(secondSavedItem.text, '第二個清單項目')