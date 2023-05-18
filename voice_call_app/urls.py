# voice_call_app/urls.py

from django.urls import path
from . import views

app_name = 'voice_call_app'

urlpatterns = [
    path('', views.index, name='index'),
]
