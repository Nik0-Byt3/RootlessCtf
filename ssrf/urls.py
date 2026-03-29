from django.urls import path
from . import views

urlpatterns = [
    path('',              views.index,         name='ssrf_index'),
    path('internal/',     views.internal,      name='ssrf_internal'),
    path('internal/flag/', views.internal_flag, name='ssrf_flag'),
]