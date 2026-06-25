from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Atividade, Meta, AtividadeDoDia
import json

dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

def index(request):
    # Obtendo todas as atividades do banco de dados
    atividades            = Atividade.objects.all()
    atividades_vinculadas = AtividadeDoDia.objects.all()
    
    dias_usados = AtividadeDoDia.objects.values_list("dia_semana",flat=True).distinct()
    dias_vazios = list(set(dias)  - set(dias_usados))
    
    return render(request,"home/index.html",{"dias": dias, "atividades": atividades, 
                                             "atividades_vinculadas": atividades_vinculadas, "dias_vazios":dias_vazios})

# View para criar/deletar atividade
def gerenciar_atividade(request):
    # Se for deletar atividades
    if request.method == "DELETE":
        data = json.loads(request.body)

        atividade_id = data.get("atividade_id")
        
        try:
            atividade = AtividadeDoDia.objects.get(id=atividade_id)
            dia = atividade.dia_semana
            atividade.delete()
            return JsonResponse({"dia": dia, "status": "ok"}, status=200)
        except Atividade.DoesNotExist:
            return JsonResponse({"erro": "Atividade não encontrada"}, status=404)
    
    # Se for adicionar atividades
    if request.method == "POST":
        data = json.loads(request.body)
        
        # Operacao de criar atividade
        atividade = Atividade.objects.create(
            nome=data["nome_atividade"],
            meta_horas=0,
            total_horas=0
        )
        return JsonResponse({"id": atividade.id, "status": "ok"})
        
    return JsonResponse({"erro": "Metodo nao permitido"}, status=405)


def associar_atividade(request):
    # Se for adicionar atividades
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            print(data["nome_atividade"])
            atividade = Atividade.objects.get(nome=data["nome_atividade"])
            
            # Operacao de associar atividade
            novo_vinculo = AtividadeDoDia.objects.create(
                dia_semana=data["dia_semana"],
                horas_feitas= float (data["horas_feitas"]),
                atividade=atividade
            )
            return JsonResponse({"status": "ok", "id": novo_vinculo.id})
        except Exception as e:
            print(f'erro? {e}')
            return JsonResponse({"erro": str(e)}, status=400)
        
    return JsonResponse({"erro": "Metodo nao permitido"}, status=405)


def metas(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            atividade = Atividade.objects.get(nome=data["id"])
            
            if data["operacao"] == "reset":
                atividade.meta_horas = 0
                atividade.save()
                return JsonResponse({"status": "ok"}, status=200)
                
        except Exception as e:
            print(f'erro? {e}')
            return JsonResponse({"erro": str(e)}, status=400)

    
    atividades = Atividade.objects.all()
    atividades_vinculadas = AtividadeDoDia.objects.all()
    metas = Meta.objects.all()

    for atividade in atividades:
        atividade.percentual = 0 if atividade.atividade_horas == 0 else min(
            int((atividade.total_horas / atividade.meta_horas) * 100),
            100
        )

    metas_atingidas = sum(1 for atividade in atividades if atividade.total_horas >= atividade.meta_horas)
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
    atividades = Atividade.objects.all()
    soma_total_minutos = sum(atv.duracao_minutos for atv in atividades)
    horas_semana = soma_total_minutos / 60
    
    dias_ativos = Atividade.objects.values('dia_semana').distinct().count()
        
    return render(request,"home/relatorios.html", {"horas_semana": horas_semana, "dias_ativos": dias_ativos})

def hoje(request):
    return render(request, "home/hoje.html")

def calendario(request):
    return render(request, "home/calendario.html")

def atividades(request):
    # Obtendo todas as atividades do banco de dados
    atividades = Atividade.objects.all()
    
    
    return render(request, "home/atividades.html", {"atividades":atividades})