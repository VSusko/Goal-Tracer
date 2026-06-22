from django.shortcuts import render
from django.http import JsonResponse
from .models import Atividade
import json


dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

def index(request):    

    # Obtendo todas as atividades do banco de dados
    atividades = Atividade.objects.all()
    
    # Convertendo a duração de minutos para horas e armazenando em um atributo temporário
    for atividade in atividades:
        atividade.duracao_horas = atividade.duracao_minutos / 60.0

    # Criando uma lista para armazenar os dias da semana e suas atividades
    atividades_por_dia = []
    
    # Para cada dia, verifica se existe uma atividade
    for dia in dias:
        # Filtra as atividades e coloca na lista apenas as que correspondem ao dia atual
        lista = [a for a in atividades if a.dia_semana == dia]
        
        # Adiciona a lista gerada
        atividades_por_dia.append((dia, lista))

    return render(request,"home/index.html",{"dias": dias, "atividades_por_dia": atividades_por_dia})

# View para criar/deletar atividade
def gerenciar_atividade(request):
    # Se for deletar atividades
    if request.method == "DELETE":
        data = json.loads(request.body)

        atividade_id = data.get("atividade_id")
        
        try:
            atividade = Atividade.objects.get(id=atividade_id)
            dia = atividade.dia_semana
            atividade.delete()
            return JsonResponse({"dia": dia, "status": "ok"}, status=200)
        except Atividade.DoesNotExist:
            return JsonResponse({"erro": "Atividade não encontrada"}, status=404)
    
    # Se for adicionar atividades
    if request.method == "POST":
        data = json.loads(request.body)

        atividade = Atividade.objects.create(
            nome=data["nome_atividade"],
            dia_semana=data["dia_semana"],
            duracao_minutos=float(data["duracao_horas"]) * 60
        )
        return JsonResponse({"id": atividade.id, "status": "ok"})

    return JsonResponse({"erro": "Método não permitido"}, status=405)

def somar_horas(request):
    if request.method == "POST":
        data = json.loads(request.body)

        dia = data.get("dia_semana")
        soma = 0
        
        for atividade in Atividade.objects.all():
            if(atividade.dia_semana == dia):
                soma += atividade.duracao_minutos
        
        soma = soma/60    
    
        return JsonResponse({"soma": soma}, status=200)
    
    return JsonResponse({"erro": "Método não permitido"}, status=405)

def metas(request):
    return render(request, "home/metas.html")

def relatorios(request):
    atividades = Atividade.objects.all()
    soma_total_minutos = sum(atv.duracao_minutos for atv in atividades)
    horas_semana = soma_total_minutos / 60
    
    dias_ativos = Atividade.objects.values('dia_semana').distinct().count()
        
    return render(request,"home/relatorios.html", {"horas_semana": horas_semana, "dias_ativos": dias_ativos})

def hoje(request):
    return render(request, "home/hoje.html")

def calendario(request):
    return render(request, "home/calendario.html")