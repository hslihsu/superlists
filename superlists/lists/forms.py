from django import forms
from lists.models import Item
from django.utils.html import escape

EMPTY_ITEM_ERROR = escape('清單項目不能空白')


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
