from django.forms import ModelForm
from django import forms  # Correctly import forms here
from .models import VlogPost
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContentForm(ModelForm):
    class Meta:
        model = None
        fields = [] 


class Vlogform(ContentForm):
    class Meta(ContentForm.Meta):
        fields = ['title', 'video_url', 'description', 'author', 'published_date', 'tags' ]

class VlogPostForm(forms.ModelForm):
    class Meta:
        model = VlogPost
        fields = ['title', 'video_url', 'description', 'author', 'published_date', 'tags']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
