from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('metas/', views.metas, name='metas'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('hoje/', views.hoje, name='hoje'),
    path('calendario/', views.calendario, name='calendario'),
    path('atividades/', views.atividades, name='atividades'),
    path("atividade/gerenciar/", views.gerenciar_atividade, name="gerenciar_atividade"),
    path("atividade/soma_horas/", views.somar_horas, name="soma_horas"),
]