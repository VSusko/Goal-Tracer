from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Atividade, Meta
import json

def index(request):    
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

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
    # Se for deletar atividades
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
    if request.method == "POST":
        if "delete_id" in request.POST:
            Meta.objects.filter(id=request.POST["delete_id"]).delete()
            return redirect("metas")

        if "add_hour_id" in request.POST:
            meta = Meta.objects.get(id=request.POST["add_hour_id"])
            meta.horas_feitas += 1
            meta.save()
            return redirect("metas")

        Meta.objects.create(
            nome=request.POST["nome"],
            meta_horas=float(request.POST["meta_horas"]),
            horas_feitas=float(request.POST["horas_feitas"])
        )
        return redirect("metas")

    metas = list(Meta.objects.all())

    for meta in metas:
        meta.percentual = 0 if meta.meta_horas == 0 else min(
            int((meta.horas_feitas / meta.meta_horas) * 100),
            100
        )

    metas_atingidas = sum(1 for meta in metas if meta.horas_feitas >= meta.meta_horas)
    progresso_medio = round(sum(meta.percentual for meta in metas) / len(metas)) if metas else 0

    if progresso_medio >= 80:
        status = "Excelente!"
    elif progresso_medio >= 50:
        status = "No caminho certo"
    else:
        status = "Precisa melhorar"

    return render(request, "home/metas.html", {
        "metas": metas,
        "metas_atingidas": metas_atingidas,
        "total_metas": len(metas),
        "progresso_medio": progresso_medio,
        "status": status,
    })

def relatorios(request):
    return render(request, "home/relatorios.html")

def hoje(request):
    return render(request, "home/hoje.html")

def calendario(request):
    return render(request, "home/calendario.html")