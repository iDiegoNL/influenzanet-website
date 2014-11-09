from django import forms
from django.utils.translation import ugettext as _

class AddPeople(forms.Form):
    name = forms.CharField(label=_('Name'), max_length=100)
    avatar = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=0)


