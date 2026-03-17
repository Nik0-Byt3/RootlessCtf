from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm , UserChangeForm
from .models import Utente
from django.forms.widgets import FileInput

class RegistrazioneForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, label='Nome')
    last_name = forms.CharField(required=True, label='Cognome')

    class Meta:
        model = Utente
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username o Email')

class ProfiloForm(forms.ModelForm):
    class Meta:
        model = Utente
        fields = ['first_name', 'last_name', 'email', 'foto_profilo']
        widgets = {
            'foto_profilo': FileInput(),
        }