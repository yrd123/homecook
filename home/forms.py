from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Vinfo, Cinfo


class VendorForm(forms.ModelForm):
    Password=forms.CharField(widget=forms.PasswordInput)
    Confirm=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Vinfo
        fields = ['Name','Username','Password','Confirm','Email','Aadhar','Code','PhoneNo','Kitchen','Address','Image']


class CustomerForm(forms.ModelForm):
    Password=forms.CharField(widget=forms.PasswordInput)
    Confirm=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Cinfo
        fields = ['Name','Username','Password','Confirm','Email','Code','PhoneNo','Address','Image']