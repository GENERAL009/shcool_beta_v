# myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import ROLE_CHOICES, Subject, Profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=16,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Username'
                               }))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Your password'
                               }))


class TeacherRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Firstname'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Lastname'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), required=False,
                                              widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'subjects')


class StudentRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
