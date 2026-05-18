from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='visitor_index'),
]