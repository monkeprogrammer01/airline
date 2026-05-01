from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class AdminUserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "is_active", "is_staff", "is_superuser")
