from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'pesel', 'bank_account', 'secondary_email', 'address', 'role')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(max_length=50,
                                 required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    bank_account = forms.CharField(max_length=25,
                                   required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    secondary_email = forms.CharField(max_length=50,
                                      required=True,
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))

    address = forms.CharField(max_length=100,
                              required=True,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'bank_account', 'secondary_email', 'address')




