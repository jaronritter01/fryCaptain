from django.forms import ModelForm, FileInput
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import CheckboxSelectMultiple

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude=['pickup', 'customer', 'transaction_id']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'groups']

class UpdateUserProfile(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CustomerSettingUpdateForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
        widgets={
            'profile_pic': FileInput()
        }

class AddMenuItem(ModelForm):
    class Meta:
        model = MenuItem
        fields ="__all__"
        widgets={
            'item_pic': FileInput()
        }
