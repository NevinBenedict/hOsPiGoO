from django import forms
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control py-1', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control py-1', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control py-1', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control py-1', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control py-1', 'placeholder': 'Phone'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control py-1', 'placeholder': 'Password'}),
        }