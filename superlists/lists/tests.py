from django.http import HttpRequest
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.shortcuts import render
from lists.views import homePage
from lists.models import Item, List
# Create your tests here.

class HomePageTest(TestCase):


    def test_root_url_resolves_to_homePage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, homePage)
        
        
class ListAndItemModelTest(TestCase):
    
    
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        firstItem = Item()
        firstItem.text = '第一個清單項目'
        firstItem.list = list_
        firstItem.save()
        
        secondItem = Item()
        secondItem.text = '第二個清單項目'
        secondItem.list = list_
        secondItem.save()
        
        savedList = List.objects.first()
        self.assertEqual(savedList, list_)
        
        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(), 2)
        
        firstSavedItem = savedItems[0]
        secondSavedItem = savedItems[1]
        self.assertEqual(firstSavedItem.text, '第一個清單項目')
        self.assertEqual(firstSavedItem.list, list_)
        self.assertEqual(secondSavedItem.text, '第二個清單項目')
        self.assertEqual(secondSavedItem.list, list_)


class ListViewTest(TestCase):
    
    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)
        response = self.client.get(reverse('lists:viewList'))
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        
    def test_use_list_template(self):
        response = self.client.get(reverse('lists:viewList'))
        self.assertTemplateUsed(response, 'lists/list.html')


class NewListTest(TestCase):


    def test_saving_a_POST_request(self):
        self.client.post('/lists/new/', data={'itemText':'新的項目'})
        self.assertEqual(Item.objects.count(), 1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, '新的項目')


    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new/', data={'itemText':'新的項目'})
        self.assertRedirects(response, reverse('lists:viewList'))