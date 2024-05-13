from django import forms
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput,
        label='Пароль'
    )
    password2 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput,
        label='Повторите пароль'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совподают.')
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        try:
            User.objects.get(email=cd['email'])
        except User.DoesNotExist:
            return cd['email']
        raise forms.ValidationError(
            'Пользователь с такой почтой уже зарегистрирован.'
            )


class EditProfileFormUserData(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


class EditProfileFormProfileData(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'profile_image',
            'date_of_birth'
        )
