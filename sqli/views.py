import sqlite3
import os
from django.shortcuts import render
from django.conf import settings

# Percorso del DB SQLite dedicato alla sfida
DB_PATH = os.path.join(settings.BASE_DIR, 'sqli', 'sqli_challenge.db')

FLAG = 'KEY{sql_1s_s0_class1c}'


def init_db():
    """Inizializza il DB con la tabella dipendenti e alcuni utenti finti."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dipendenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            ruolo TEXT NOT NULL
        )
    ''')
    # Inserisce utenti solo se la tabella è vuota
    cursor.execute('SELECT COUNT(*) FROM dipendenti')
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            'INSERT INTO dipendenti (username, password, ruolo) VALUES (?, ?, ?)',
            [
                ('marco.rossi',   'Tr0ub4dor&3',   'developer'),
                ('giulia.bianchi', 'C0rr3ct-H0rs3', 'designer'),
                ('luca.verdi',    'P@ssw0rd!99',   'sysadmin'),
                ('admin',         'hunter2',        'admin'),
            ]
        )
    conn.commit()
    conn.close()


def login_view(request):
    init_db()
    error = None
    user = None

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            # Query vulnerabile — concatenazione diretta
            query = f"SELECT * FROM dipendenti WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            user = cursor.fetchone()
            conn.close()
        except Exception as e:
            error = f'Errore database: {e}'

        if user:
            request.session['sqli_user'] = user[1]
            request.session['sqli_ruolo'] = user[3]
            from django.shortcuts import redirect
            return redirect('sqli_dashboard')
        else:
            error = 'Credenziali non valide. Accesso negato.'

    return render(request, 'sqli/login.html', {'error': error})


def dashboard_view(request):
    sqli_user = request.session.get('sqli_user')
    if not sqli_user:
        from django.shortcuts import redirect
        return redirect('sqli_login')

    ruolo = request.session.get('sqli_ruolo', '')
    flag = FLAG if ruolo == 'admin' else None

    return render(request, 'sqli/dashboard.html', {
        'username': sqli_user,
        'ruolo': ruolo,
        'flag': flag,
    })


def logout_view(request):
    request.session.pop('sqli_user', None)
    request.session.pop('sqli_ruolo', None)
    from django.shortcuts import redirect
    return redirect('sqli_login')