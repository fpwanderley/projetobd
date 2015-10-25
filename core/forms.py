# -*- coding: utf-8 -*-

from django import forms

class LoginForm(forms.Form):

    username = forms.CharField(label = 'Usuário',
                               max_length='30',
                               required=True)

    password = forms.CharField(label = 'Usuário',
                               max_length='30',
                               required=True,
                               widget=forms.PasswordInput)
