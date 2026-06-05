from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('metas/', views.metas, name='metas'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('hoje/', views.hoje, name='hoje'),
    path('calendario/', views.calendario, name='calendario'),
]