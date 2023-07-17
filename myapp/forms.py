from django import forms
from .models import usuario, Confesion

class LoginForm(forms.Form):
    username = forms.CharField(label='username')


class Mensaje(forms.Form):
    mensaje = forms.CharField(label='Deja tu mensaje aqui', widget=forms.TextInput(
        attrs={'class': 'inputMsj'}))