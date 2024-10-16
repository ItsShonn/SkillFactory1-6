from django.contrib.admin.utils import lookup_field
from django_filters import FilterSet, CharFilter, DateFilter
from django import forms
from .models import Post, PostCategory


class DateInput(forms.DateInput):
    input_type = 'date'

class NewsFilter(FilterSet):

   title = CharFilter(field_name='title', lookup_expr='icontains')
   author = CharFilter(field_name='author__username__username', lookup_expr='icontains')
   date = DateFilter(widget=DateInput(attrs={'placeholder': 'DD/MM/YYYY'}), lookup_expr='gt')

   class Meta:
       model = Post

       fields = [
           'title', 'author', 'date'
       ]


class CategoryFilter(FilterSet):

    class Meta:
        model = Post

        categories = CharFilter(field_name='categories', lookup_expr='exact')

        fields = [
            'categories',
        ]