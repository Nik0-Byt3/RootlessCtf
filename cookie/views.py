import base64
from django.shortcuts import render

FLAG = 'KEY{n3v3r_trust_th3_cl13nt}'


def home(request):
    """Homepage e-commerce — assegna cookie usr_ctx=user al primo accesso."""
    prodotti = [
        {'nome': 'Cuffie Pro X',     'prezzo': '89.99',  'emoji': '🎧'},
        {'nome': 'Tastiera Meccanica', 'prezzo': '129.99', 'emoji': '⌨️'},
        {'nome': 'Webcam HD',         'prezzo': '59.99',  'emoji': '📷'},
    ]
    response = render(request, 'cookie/home.html', {'prodotti': prodotti})
    response.set_cookie('sys_info', base64.b64encode(b'KEY{c00k13s_4r3_t4sty}').decode())  # ← aggiungi qu
    if not request.COOKIES.get('usr_ctx'):
        response.set_cookie('usr_ctx', base64.b64encode(b'user').decode())

    return response


def premio(request):
    """Pagina premio — accessibile solo se cookie usr_ctx decodificato = admin."""
    usr_ctx = request.COOKIES.get('usr_ctx', '')

    try:
        role = base64.b64decode(usr_ctx).decode()
    except Exception:
        role = 'user'

    if role == 'admin':
        return render(request, 'cookie/premio.html', {'flag': FLAG})

    return render(request, 'cookie/accesso_negato.html')