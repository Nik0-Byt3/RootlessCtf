from django.urls import path
from . import views

# Definiamo l'app_name per il namespace degli URL
app_name = 'cryptography'

urlpatterns = [
    # Pagina principale dell'app (opzionale, se vuoi un elenco)
    path('', views.crypto_index, name='index'),

    # Link semplificati per le sfide (da inserire nel campo 'link' del DB)
    path('vigenere/', views.sfida_vigenere, name='sfida_vigenere'),
    path('xor-reuse/', views.sfida_xor, name='sfida_xor'),
    path('rsa-low-exponent/', views.sfida_rsa, name='sfida_rsa'),
    path('hash-extension/', views.sfida_hash, name='sfida_hash'),
]