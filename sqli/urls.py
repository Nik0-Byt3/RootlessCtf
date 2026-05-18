from django.urls import path
from . import views

urlpatterns = [
    path('',          views.login_view,    name='sqli_login'),
    path('dashboard/', views.dashboard_view, name='sqli_dashboard'),
    path('logout/',    views.logout_view,    name='sqli_logout'),
]