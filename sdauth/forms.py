# This Python file uses the following encoding: utf-8
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from sdauth.models import User


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Contraseña",
                                         help_text="Raw passwords are not stored, so there is no way to see "
                                                   "this user's password, but you can change the password "
                                                   "using <a href=\"password/\">this form</a>.")

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial.get('password')

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        password = self.cleaned_data['password']
        if password in ['', None]:
            user.set_unusable_password()
        if commit:
            user.save()
        return user


class AuthForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super(AuthForm, self).__init__(request, *args, **kwargs)

        self.fields['username'].widget = forms.EmailInput(attrs={
            'placeholder': 'Correo',
            'autofocus': 'true',
            'class': 'form-control',
            'required': 'true'
        })
        self.fields['username'].label = ''
        self.fields['username'].required = True

        self.fields['password'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'form-control',
            'required': 'true',
            'autocomplete': 'off'
        })
        self.fields['password'].label = ''
        self.fields['password'].required = True

    def confirm_login_allowed(self, user):
        pass

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if email and password:
            params = dict(username=email, password=password, request=self.request)
            self.user_cache = authenticate(**params)

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': 'email'},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data