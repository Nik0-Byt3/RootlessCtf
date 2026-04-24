from django.shortcuts import render, get_object_or_404
from main.models import Sfida, Categoria

# Funzione helper per evitare ripetizioni di codice
def get_crypto_challenge(search_term):
    """Recupera la sfida che contiene la parola chiave nel titolo"""
    return get_object_or_404(Sfida, titolo__icontains=search_term)

def crypto_index(request):
    """Pagina principale della categoria Cryptography (opzionale)"""
    categoria = get_object_or_404(Categoria, nome__iexact='Cryptography')
    sfide = Sfida.objects.filter(categoria=categoria).order_by('id')
    return render(request, 'cryptography/index.html', {'sfide': sfide})

# --- VIEW DELLE SINGOLE SFIDE ---

def sfida_vigenere(request):
    sfida = get_crypto_challenge('Vigenère')
    return render(request, 'cryptography/sfida_vigenere.html', {'sfida': sfida})

def sfida_xor(request):
    sfida = get_crypto_challenge('XOR')
    return render(request, 'cryptography/sfida_xor.html', {'sfida': sfida})

def sfida_rsa(request):
    sfida = get_crypto_challenge('RSA')
    return render(request, 'cryptography/sfida_rsa.html', {'sfida': sfida})

def sfida_hash(request):
    sfida = get_crypto_challenge('Hash')
    return render(request, 'cryptography/sfida_hash.html', {'sfida': sfida})