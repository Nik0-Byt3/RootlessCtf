from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Categoria, Sfida, Flag, Indizio, Profilo, Partecipa, FileSfida

class ProfiloInline(admin.StackedInline):
    model = Profilo
    can_delete = False
    verbose_name_plural = 'Profilo CTF'
    filter_horizontal = ('flag',)

class PersonalizzatoUserAdmin(UserAdmin):
    inlines = (ProfiloInline,)

admin.site.unregister(User)
admin.site.register(User, PersonalizzatoUserAdmin)

admin.site.register(Categoria)
admin.site.register(Sfida)
admin.site.register(Flag)
admin.site.register(Indizio)
admin.site.register(Partecipa)
admin.site.register(FileSfida)