from django import forms
from django.utils.html import escape
from django.core.exceptions import ValidationError
from lists.models import Item


EMPTY_ITEM_ERROR = escape('清單項目不能空白')
DUPLICATE_ITEM_ERROR = escape('你的清單中已有此項目')

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text':forms.fields.TextInput(attrs={
                'placeholder':'輸入一個待辦項目',
                'class':'form-control input-lg'
            }),
        }
        
        error_messages = {
            'text':{'required':EMPTY_ITEM_ERROR}
        } 
        
    def save(self, forList):
        self.instance.list = forList
        return super().save()


class ExistingListItemForm(ItemForm):
    def __init__(self, forList, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = forList
    
    
    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text':[DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
            
    def save(self):
        return forms.ModelForm.save(self)