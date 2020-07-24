from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm


gender_choices = [
    ('male','Male'),
    ('female','Female'),
    ('not_tell','Ain\'t Gonna Tell Ya.')
]


class UserRegisterForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    gender = forms.CharField(label='What\'s your gender?', widget=forms.Select(choices=gender_choices))
    phone = forms.CharField(label='Phone')

    class Meta:
        # Configuration
        model = User
        # prompt order
        fields = ['username', 'phone', 'gender', 'password1', 'password2']