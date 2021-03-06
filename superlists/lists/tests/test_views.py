from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from lists.views import homePage
from lists.models import Item, List
from django.utils.html import escape
from lists.forms import ItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm
# Create your tests here.


class HomePageTest(TestCase):

        
    def test_homePage_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')
        
        
    def test_homePage_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)
        

class ListViewTest(TestCase):
    
    
    def test_displays_only_items_for_that_list(self):
        correctList = List.objects.create()
        Item.objects.create(text='itemey 1', list=correctList)
        Item.objects.create(text='itemey 2', list=correctList)
        otherList = List.objects.create()
        Item.objects.create(text='other list item 1', list=otherList)
        Item.objects.create(text='other list item 2', list=otherList) 
        response = self.client.get(reverse('lists:viewList', args=(correctList.id, )))
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')
        
        
    def test_use_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(reverse('lists:viewList', args=(list_.id, )))
        self.assertTemplateUsed(response, 'lists/list.html')
        
    
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(reverse('lists:viewList', args=(list_.id, )), data={'text':''})


    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)
    
    
    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')


    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)


    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response,EMPTY_ITEM_ERROR)


    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(reverse('lists:viewList', args=(list_.id, )))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')
        
        
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='textey')
        response = self.client.post(reverse('lists:viewList', args=(list_.id, )), data={'text':'textey'})
        expectError = escape('你的清單中已有此項目')
        self.assertContains(response, expectError)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertEqual(Item.objects.count(), 1)


class NewListTest(TestCase):
    
    
    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post(reverse('lists:newList'), data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')


    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post(reverse('lists:newList'), data={'text':''})
        self.assertContains(response, EMPTY_ITEM_ERROR)
        
    
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post(reverse('lists:newList'), data={'text':''})
        self.assertIsInstance(response.context['form'], ItemForm)


    def test_saving_a_POST_request(self):
        self.client.post(reverse('lists:newList'), data={'text':'新的項目'})
        self.assertEqual(Item.objects.count(), 1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, '新的項目')


    def test_redirect_after_POST(self):
        response = self.client.post(reverse('lists:newList'), data={'text':'新的項目'})
        newList = List.objects.first()
        self.assertRedirects(response, reverse('lists:viewList', args=(newList.id, )))
        

class ExistingListItemFormTest(TestCase):
    
    
    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(forList=list_)
        self.assertIn('placeholder="輸入一個待辦項目"', form.as_p())


    def test_form_validation_for_blank_item(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(forList=list_, data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])


    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        text = '沒有雙胞胎'
        Item.objects.create(list=list_, text=text)
        form = ExistingListItemForm(forList=list_, data={'text':text})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])
        
        
    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(forList=list_, data={'text':'Hi'})
        newItem = form.save()
        self.assertEqual(newItem, Item.objects.first())