from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomuserCreationForm(UserCreationForm):
    password1 = forms.CharField(
    label="Password",
    strip=False,
    widget=forms.PasswordInput,
    # help_text=password_validation.password_validators_help_text_html(),
)
    password2 = forms.CharField(
    label="Password confirmation",
    widget=forms.PasswordInput,
    strip=False,
    help_text="Enter the same password as before, for verification.",
    )


    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    # def clean(self):
    #     user = User.objects.get(email=self.email)
        
    #     if user is not None:
    #         return ValidationError("email exist")
        
    #     return super().clean()