from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('metas/', views.metas, name='metas'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('hoje/', views.hoje, name='hoje'),
    path('calendario/', views.calendario, name='calendario'),
    path('atividades/', views.atividades, name='atividades'),
    path("atividade/gerenciar/", views.gerenciar_atividade, name="gerenciar_atividade"),
    path("atividade/associar/", views.associar_atividade, name="associar_atividade"),
    path("atividade/atualizar_horas/", views.atualizar_horas, name="atualizar_horas"),
    path("atividade/atualizar-horas-hoje/", views.atualizar_horas_hoje, name="atualizar_horas_hoje"),
    path("login/", auth_views.LoginView.as_view(template_name="home/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
]