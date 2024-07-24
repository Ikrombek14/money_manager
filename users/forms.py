# forms.py
from django import forms
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label='New Password'
    )

    class Meta:
        model = User
        fields = ['username']  # List of fields to include in the form

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")

        if new_password:
            if len(new_password) < 8:
                self.add_error('new_password', 'Password must be at least 8 characters long.')
        return cleaned_data
