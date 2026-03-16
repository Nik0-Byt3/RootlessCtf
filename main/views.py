from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegistrazioneForm, LoginForm , ProfiloForm
from django.contrib.auth.decorators import login_required
from .models import Utente, Sfida, Flag, Categoria, Indizio, Partecipa
from django.contrib.auth.forms import PasswordChangeForm

def home(request):
    return render(request, 'main/home.html')

def registrazione(request):
    if request.method == 'POST':
        form = RegistrazioneForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = RegistrazioneForm()
    return render(request, 'main/registrazione.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'main/login.html', {'form': form, 'errore': 'Credenziali errate: username o password invalidi'})
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html', {'utente': request.user})

@login_required
def catalogo(request):
    sfide = Sfida.objects.all()
    return render(request, 'main/catalogo.html', {'sfide': sfide})

@login_required
def sfida_detail(request, id):
    sfida = Sfida.objects.get(id=id)
    flags = Flag.objects.filter(sfida=sfida)
    return render(request, 'main/sfida_detail.html', {'sfida': sfida, 'flags': flags})

@login_required
def profilo(request):
    if request.method == 'POST':
        form = ProfiloForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profilo')
    else:
        form = ProfiloForm(instance=request.user)
    return render(request, 'main/profilo.html', {'form': form})

@login_required
def cambio_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'main/cambio_password.html', {'form': form})