from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase
from lists.models import Item, List


# Create your tests here.
class ListModelTest(TestCase):
    
    
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), reverse('lists:viewList', args=(list_.id, ))) 


class ItemModelTest(TestCase):
    
    
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')
    
    
    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())
    
    
    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean() 
            
    
    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()
            
            
    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()    # Should not raise
        
        
    def test_list_ordering(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text='第1個')
        item2 = Item.objects.create(list=list_, text='第2個')
        item3 = Item.objects.create(list=list_, text='第3個')
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])