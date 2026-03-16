from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registrazione/', views.registrazione, name='registrazione'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('sfida/<int:id>/', views.sfida_detail, name='sfida_detail'),
    path('profilo/', views.profilo, name='profilo'),
    path('cambio-password/', views.cambio_password, name='cambio_password'),
]