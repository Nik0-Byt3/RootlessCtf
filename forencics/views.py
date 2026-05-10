from django.shortcuts import render, get_object_or_404
from main.models import Sfida
from django.contrib.auth.decorators import login_required

@login_required
def metadati_exif(request):
    sfida = get_object_or_404(Sfida, titolo='Metadati EXIF')

    context = {
        'sfida': sfida,
        'challenge_name': sfida.titolo,
        'challenge_id': sfida.id,
        'evidence_id': "EVD-2026-772",
        'md5_hash': "e99a18c428cb38d5f260853678922e03",
    }

    return render(request, 'forencics/metadati_exif.html', context)

@login_required
def sfida_matriosca(request):
    sfida = get_object_or_404(Sfida, titolo='Archivio Fantasma')
    context = {
        'sfida': sfida,
        'challenge_name': sfida.titolo,
        'difficulty': "Media",
        'osint_target': "Unknown Vendor",
        'protocol': "BINARY-CARVING-V1",
    }
    return render(request, 'forencics/sfida_matriosca.html', context)


@login_required
def sfida_network_view(request):
    sfida = get_object_or_404(Sfida, titolo='Intercettazione di Rete')

    return render(request, 'forencics/sfida_network.html', {
        'sfida': sfida,
    })