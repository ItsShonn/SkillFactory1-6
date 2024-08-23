from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Post


class NewsForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'author', 'content', 'categories']