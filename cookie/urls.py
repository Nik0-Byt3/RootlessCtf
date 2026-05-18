from django.urls import path
from . import views

urlpatterns = [
    path('',        views.home,   name='cookie_home'),
    path('premio/', views.premio, name='cookie_premio'),
]