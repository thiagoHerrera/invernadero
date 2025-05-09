from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': ''})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': ''})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': ''})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': ''}) 
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está en uso.")
        return email
