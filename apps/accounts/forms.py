from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User
from helpers.validators import validate_password_not_similar_to_email


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email']


class UserForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['name', 'email','password1', 'password2']

        widgets = {
            'password1': forms.TextInput(attrs={'class': 'form-control', 'type':'password'}),
            'password2': forms.EmailInput(attrs={'class': 'form-control', 'type':'password'}),
        }
        
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', 'Senha e Confirme sua senha não são iguais.')
            
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        email = self.cleaned_data.get('email')
        password1 = validate_password_not_similar_to_email(password1, email)
        return password1
