from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # IMPORTANTE: Usiamo l'User standard di Django
from django.forms.widgets import FileInput
from .models import Profilo  # Importiamo il nuovo modello del Profilo


# 1. FORM DI REGISTRAZIONE
class RegistrazioneForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, label='Nome')
    last_name = forms.CharField(required=True, label='Cognome')

    class Meta:
        model = User  # Cambiato da Utente a User standard
        fields = ['username', 'first_name', 'last_name',
                  'email']  # Rimosse password1/2 (vengono gestite automaticamente da UserCreationForm)


# 2. FORM DI LOGIN (Resta identico, ma punta a User implicitamente)
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username o Email')


# 3. FORM DEL PROFILO (Unione dei campi User + campi Profilo)
class ProfiloForm(forms.ModelForm):
    # Definiamo esplicitamente i campi dell'User che vogliamo modificare nella stessa pagina
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=150, required=True, label='Cognome')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = Profilo  # Cambiato da Utente a Profilo
        fields = ['foto_profilo']  # Qui inseriamo solo i campi del modello Profilo
        widgets = {
            'foto_profilo': FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se stiamo modificando un profilo esistente, popoliamo i campi dell'User collegato
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        # 1. Salviamo prima i dati del profilo
        profilo = super().save(commit=False)

        # 2. Aggiorniamo a mano l'utente collegato a questo profilo
        user = profilo.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            profilo.save()
        return profilo