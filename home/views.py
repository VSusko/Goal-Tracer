from django.shortcuts import render
from .models import Mensagem


def index(request):
    mensagens = Mensagem.objects.all()
    return render(request, "home/index.html", {"mensagens": mensagens})

def metas(request):
    return render(request, "home/metas.html")

def relatorios(request):
    return render(request, "home/relatorios.html")

def hoje(request):
    return render(request, "home/hoje.html")

def calendario(request):
    return render(request, "home/calendario.html")