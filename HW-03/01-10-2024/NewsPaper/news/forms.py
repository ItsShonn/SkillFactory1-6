from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from .models import Post


class NewsForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'author', 'content', 'categories']


"""class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
"""