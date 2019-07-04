from django import forms

from .models import ItemCount


class SetItemCountForm(forms.ModelForm):
    class Meta:
        model = ItemCount