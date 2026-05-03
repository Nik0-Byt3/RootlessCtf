from django.shortcuts import render

FLAG = 'KEY{0n3_th0usand_v1s1t0rs}'
SPECIAL_VISITOR = 1000


def index(request):
    """Pagina principale — legge X-Visitor-ID dall'header o dal cookie."""

    # Prova prima l'header, poi il cookie
    visitor_id = request.META.get('HTTP_X_VISITOR_ID') or request.COOKIES.get('X-Visitor-ID', '')

    try:
        visitor_num = int(visitor_id)
    except (ValueError, TypeError):
        visitor_num = None

    flag = None
    is_special = False

    if visitor_num == SPECIAL_VISITOR:
        flag = FLAG
        is_special = True

    response = render(request, 'visitor/index.html', {
        'visitor_num': visitor_num,
        'is_special': is_special,
        'flag': flag,
    })

    response['X-Secret'] = 'KEY{h34d3rs_4r3_s3cr3t}'

    return response