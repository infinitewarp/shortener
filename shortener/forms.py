from django import forms
from django.utils.translation import ugettext_lazy as _


class LinkForm(forms.Form):
    url = forms.URLField(
        label=_('Long URL'),
        max_length=2000,
        widget=forms.TextInput(
            attrs={
                'type': 'url',
                'required': True,
                'class': 'form-control',
                'placeholder': 'http://',
                'autocomplete': 'off',
            }
        )
    )
