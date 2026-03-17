from django.shortcuts import render, redirect , get_object_or_404
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
    categorie = Categoria.objects.all()
    utente = request.user

    # Filtri
    categoria = request.GET.get('categoria')
    difficolta = request.GET.get('difficolta')
    stato = request.GET.get('stato')

    if categoria:
        sfide = sfide.filter(categoria__id=categoria)
    if difficolta:
        sfide = sfide.filter(difficolta=difficolta)

    # Annota ogni sfida con lo stato dell'utente
    partecipazioni = Partecipa.objects.filter(utente=utente).values('sfida_id', 'stato')
    stato_map = {p['sfida_id']: p['stato'] for p in partecipazioni}

    risultati = []
    for sfida in sfide:
        sfida.stato_utente = stato_map.get(sfida.id, 'non_iniziata')
        if not stato or sfida.stato_utente == stato:
            risultati.append(sfida)

    return render(request, 'main/catalogo.html', {
        'sfide': risultati,
        'categorie': categorie,
    })

@login_required
def sfida_detail(request, id):
    sfida = get_object_or_404(Sfida, id=id)
    flags = Flag.objects.filter(sfida=sfida)
    utente = request.user
    partecipa, _ = Partecipa.objects.get_or_create(utente=utente, sfida=sfida)

    flags_corrette = set(utente.flag.filter(sfida=sfida).values_list('id', flat=True))
    indizi_sbloccati = set(partecipa.indizi_sbloccati.values_list('flag_id', flat=True))
    flag_feedback_id = flag_ok = indizio_sbloccato = None
    sfida_appena_completata = False  # dichiarato qui, sempre disponibile

    if request.method == 'POST':
        if partecipa.stato == 'non_iniziata':
            partecipa.stato = 'incompleta'
            partecipa.save()

        flag = get_object_or_404(Flag, id=request.POST.get('flag_id'), sfida=sfida)

        if request.POST.get('sblocca_indizio_id'):
            indizio = Indizio.objects.filter(flag=flag).first()
            if indizio and flag.id not in indizi_sbloccati:
                partecipa.indizi_sbloccati.add(indizio)
                partecipa.punteggio_ottenuto = max(0, partecipa.punteggio_ottenuto - 5)
                partecipa.save()
                indizi_sbloccati.add(flag.id)
            indizio_sbloccato = True

        else:
            flag_input = request.POST.get('flag_input', '').strip()
            flag_feedback_id = flag.id
            if flag_input == flag.chiave and flag.id not in flags_corrette:
                utente.flag.add(flag)
                flags_corrette.add(flag.id)
                flag_ok = True
                if flags_corrette >= set(flags.values_list('id', flat=True)):
                    sfida_appena_completata = True
                    partecipa.stato = 'completata'
                    partecipa.punteggio_ottenuto = max(0, sfida.p_massimo - partecipa.indizi_sbloccati.count() * 5)
                    utente.punteggio += partecipa.punteggio_ottenuto
                    utente.livello = 'esperto' if utente.punteggio >= 600 else 'intermedio' if utente.punteggio >= 350 else 'principiante'
                    utente.save()
                    partecipa.save()
            else:
                flag_ok = False

    return render(request, 'main/sfida_detail.html', {
        'sfida': sfida,
        'flags': flags,
        'flags_corrette': flags_corrette,
        'indizi_sbloccati': indizi_sbloccati,
        'flag_feedback_id': flag_feedback_id,
        'flag_ok': flag_ok,
        'challenge_started': partecipa.stato != 'non_iniziata',
        'indizio_sbloccato': indizio_sbloccato,
        'sfida_completata': partecipa.stato == 'completata' and not sfida_appena_completata,
        'sfida_appena_completata': sfida_appena_completata,
        'partecipa_punteggio': partecipa.punteggio_ottenuto,
    })

@login_required
def profilo(request):
    if request.method == 'POST':
        form = ProfiloForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
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