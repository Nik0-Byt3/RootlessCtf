from django.shortcuts import render, get_object_or_404
from main.models import Sfida, Categoria
import hashlib


# Parametri segreti (nascosti all'utente)
SECRET = b"S3CR3T_K3Y_123"  # Lunghezza 14
ORIGINAL_DATA = b"user=guest&role=read"
FLAG = "KEY{md5_padding_oracle}"


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
    # Calcoliamo la firma originale da mostrare all'utente
    original_sig = hashlib.md5(SECRET + ORIGINAL_DATA).hexdigest()

    result = None
    alert_type = "info"

    if request.method == "POST":
        p_hex = request.POST.get("payload_hex", "").strip()
        p_sig = request.POST.get("signature", "").strip()

        try:
            # Convertiamo l'input HEX dell'utente in byte
            payload_bytes = bytes.fromhex(p_hex)

            # Il server ricalcola l'hash: MD5(SECRET + PAYLOAD_RICEVUTO)
            expected_sig = hashlib.md5(SECRET + payload_bytes).hexdigest()

            # Validazione
            if expected_sig == p_sig:
                if b"role=admin" in payload_bytes:
                    result = f"Accesso Admin Garantito! Flag: {FLAG}"
                    alert_type = "success"
                else:
                    result = "Firma valida, Errore nei permessi utente "
                    alert_type = "warning"
            else:
                result = "Firma non valida! L'attacco di estensione è fallito."
                alert_type = "danger"
        except (ValueError, TypeError):
            result = "Errore: Inserisci un payload HEX valido."
            alert_type = "danger"

    context = {
        'sfida' : sfida ,
        'original_data': ORIGINAL_DATA.decode(),
        'original_sig': original_sig,
        'result': result,
        'alert_type': alert_type,
    }
    return render(request, 'cryptography/sfida_hash.html', context)