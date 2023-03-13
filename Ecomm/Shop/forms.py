from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, \
    PasswordResetForm, SetPasswordForm
from django.db import models
from django.forms import PasswordInput
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime

from .models import PaymentOption, Comment, Product, CommentReply
from .models import Customer, Payment
from django import forms


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    PasswordInput(attrs={'class': 'form-control'})


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(
        attrs={'autofocus': 'True', 'autocomplete': 'current-password', 'class': 'form-control'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'locality', 'city', 'mobile', 'area', 'zipcode']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.NumberInput(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PaymentOptionForm(forms.Form):
    payment_option = forms.ModelChoiceField(
        queryset=PaymentOption.objects.all(),
        widget=forms.RadioSelect
    )


class ProductSearchForm(forms.Form):
    search_query = forms.CharField(label='Search query', max_length=100)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['id', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control h-25', 'placeholder': "Write your comment"}),
        }

    parent_comment = forms.ModelChoiceField(queryset=Comment.objects.all(), widget=forms.HiddenInput, required=False)


class ReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ('description', 'parent')
        widgets = {
            'parent': forms.HiddenInput(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Write your reply"}),
        }

