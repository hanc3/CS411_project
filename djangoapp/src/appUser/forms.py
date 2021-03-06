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
    email = forms.EmailField(label='Email')

    class Meta:
        # Configuration
        model = User
        # prompt order
        fields = ['username', 'phone', 'email', 'gender', 'password1', 'password2']


class apartmentForm(forms.Form):
    apartment_name = forms.CharField(widget=forms.TextInput(attrs={'name': 'Apartment Name'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'description': 'Description'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'address': 'Address'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'email':'Email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'phone': 'Phone'}))
    pet = forms.BooleanField(required=False)
    printer = forms.BooleanField(required=False)
    pool = forms.BooleanField(required=False)
    gym = forms.BooleanField(required=False)


class updateProfile(forms.Form):
    bio = forms.CharField(widget=forms.TextInput(attrs={'bio': 'bio'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'email':'Email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'phone': 'Phone'}))
    gender = forms.CharField(label='What\'s your gender?', widget=forms.Select(choices=gender_choices))
