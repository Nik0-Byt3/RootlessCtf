from django.urls import path
from . import views

app_name = 'forencics'

urlpatterns = [
    # Rotta specifica per la Sfida 09
    path('casi/analisi-metadati/', views.metadati_exif, name='metadati_exif'),
    path('casi/matriosca/', views.sfida_matriosca, name='sfida_matriosca'),
    path('casi/network-forensics/', views.sfida_network_view, name='sfida_network'),
    # path('casi/steganografia-lsb/', views.steganografia_lsb, name='steganografia_lsb'),
]