from django.shortcuts import render
from .models import Atividade


def index(request):
    # atividades = Atividade.objects.all()
    # dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

    # return render(request,"home/index.html",{"atividades": atividades, "dias_semana": dias_semana})
    dias = []

    for nome_dia in ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"] : dias.append({"nome": nome_dia,
        "atividades": Atividade.objects.filter(dia_semana=nome_dia)})
    return render(request,"home/index.html",{"dias": dias})

def metas(request):
    return render(request, "home/metas.html")

def relatorios(request):
    return render(request, "home/relatorios.html")

def hoje(request):
    return render(request, "home/hoje.html")

def calendario(request):
    return render(request, "home/calendario.html")