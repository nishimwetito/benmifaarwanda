from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label,
            })


class AdminMemberForm(RegisterForm):
    """Staff-only form to register platform members."""

    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    phone_number = forms.CharField(max_length=20, required=False, label='Phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'e.g. +250 788 000 000'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.username.lower()
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            profile = user.profile
            phone = self.cleaned_data.get('phone_number', '')
            if phone:
                profile.phone_number = phone
                profile.save(update_fields=['phone_number'])
        return user
