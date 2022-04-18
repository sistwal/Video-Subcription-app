from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class signup(UserCreationForm):
 
 email=forms.EmailField(max_length=50)
 class Meta:
    model=User
    fields=['username','email','password1']
    labels={'username':'Username'}
    widgets={
       'password1':forms.PasswordInput(attrs={'class':'form-control'})}

