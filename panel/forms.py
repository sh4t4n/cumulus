# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

class CreateUserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email']
        
class UpdateUserForm(forms.ModelForm):

    email = forms.CharField(max_length=75, required=True)    
    first_name = forms.CharField(min_length=3, max_length=25, required=True) 
    last_name = forms.CharField(min_length=3, max_length=25, required=True)  
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']