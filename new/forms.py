from django import forms
from .models import Likee


class Like(forms.ModelForm):
    like = forms.BooleanField(label='Поставишь лайк?')
