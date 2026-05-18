import base64
from django.shortcuts import render
from django.http import HttpResponse
from playwright.sync_api import sync_playwright

FLAG = 'KEY{r3qu3st_fr0m_1ns1d3}'


def index(request):
    """Homepage con il tool di screenshot URL."""
    screenshot = None
    error = None
    url = ''

    if request.method == 'POST':
        url = request.POST.get('url', '').strip()
        if url:
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(args=['--no-sandbox', '--disable-dev-shm-usage'])
                    page = browser.new_page()
                    page.goto(url, timeout=5000)
                    img_bytes = page.screenshot(full_page=True)
                    browser.close()
                screenshot = base64.b64encode(img_bytes).decode()
            except Exception as e:
                error = f'Impossibile raggiungere il sito: {e}'

    return render(request, 'ssrf/index.html', {
        'screenshot': screenshot,
        'error': error,
        'url': url,
        'examples': ['https://example.com', 'https://wikipedia.org', 'https://github.com'],
    })


def internal(request):
    """Rotta interna — non accessibile direttamente dall'esterno."""
    ip = request.META.get('REMOTE_ADDR', '')
    if ip != '127.0.0.1':
        return HttpResponse('403 Forbidden', status=403)
    return render(request, 'ssrf/internal.html')


def internal_flag(request):
    """Rotta con la flag — accessibile solo dal server stesso."""
    ip = request.META.get('REMOTE_ADDR', '')
    if ip != '127.0.0.1':
        return HttpResponse('403 Forbidden', status=403)
    return render(request, 'ssrf/flag.html', {'flag': FLAG})