from django.contrib import admin
from .models import Utente, Categoria, Sfida, Flag, Indizio, Partecipa
from django.contrib.auth.admin import UserAdmin


class UtenteAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informazioni CTF', {
            'fields': ('foto_profilo', 'punteggio', 'livello', 'flag')
        }),
    )

admin.site.register(Utente, UtenteAdmin)

models = [Categoria, Sfida, Flag, Indizio, Partecipa]
for model in models:
    admin.site.register(model)


