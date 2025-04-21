# apps/voz/urls.py

from django.urls import path
from apps.voz.views import VozComandoListView, VozComandoDetailView

urlpatterns = [
    path('comandos/', VozComandoListView.as_view(), name='voz_comandos_list'),
    path('comandos/<int:comando_id>/', VozComandoDetailView.as_view(), name='voz_comandos_detail'),
]
