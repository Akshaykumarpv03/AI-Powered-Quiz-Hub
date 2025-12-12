# apps/users/forms.py — FINAL
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Role

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ("email", "full_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]
        user.full_name = self.cleaned_data.get("full_name")
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'accept': 'image/*'}))
    avatar_clear = forms.BooleanField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ['full_name', 'avatar', 'bio', 'role']

    def clean_avatar(self):
        if self.cleaned_data.get('avatar_clear'):
            return None
        return self.cleaned_data.get('avatar')