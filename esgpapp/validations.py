from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
import re

class SignUpForm(forms.Form):
    name = forms.CharField(
        max_length = 50,
    )

    email= forms.EmailField(
        validators = [validators.EmailValidator(message ='Invalid Email Address')],
        max_length= 50,
    )
    
    pnumber= forms.CharField(
        max_length= 20,
    )
    
    dob= forms.CharField(
    )
    
    fos= forms.CharField(
        max_length= 50,
    )
    
    psw= forms.CharField(
        validators =[validators.MinLengthValidator(8, message = 'Password Must be 8 characters ')],
        widget=forms.PasswordInput
    )
    
    psw_repeat= forms.CharField(
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        p1 = cleaned_data.get("psw")
        p2 = cleaned_data.get("psw_repeat")
        if p1 != p2:
            raise forms.ValidationError("password and confirm_password does not match")

class loginform(forms.Form):
    email= forms.CharField(
        validators = [validators.EmailValidator(message ='Invalid Email Address')],
        max_length= 50,
    )
    psw= forms.CharField(
        widget=forms.PasswordInput
    )