from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Form for creating a new user account
class SignUpForm(UserCreationForm):
    # Email field
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    # Username field
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )

    # Password field
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a password'
        }),
        help_text="Use at least 8 characters."
    )

    # Confirm password field
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        }),
        help_text="Enter the same password again."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']