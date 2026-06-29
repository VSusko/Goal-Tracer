from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from .models import Atividade, Meta, AtividadeDoDia
import json
from collections import defaultdict

dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

def index(request):
    # Obtendo todas as atividades do banco de dados
    atividades            = Atividade.objects.prefetch_related('vinculos_dias').all()
    atividades_vinculadas = AtividadeDoDia.objects.all()
    
    dias_usados = AtividadeDoDia.objects.values_list("dia_semana",flat=True).distinct()
    dias_vazios = list(set(dias)  - set(dias_usados))
    
    soma_por_dia = defaultdict(float)
    for atividade in atividades_vinculadas:
        soma_por_dia[atividade.dia_semana] += atividade.horas_feitas
        
    total_horas_por_dia = [soma_por_dia[dia] for dia in dias]
    
    dias_horas = zip(dias, total_horas_por_dia)
    
    metas = Meta.objects.all()
    for meta in metas:
        meta.horas_semana = AtividadeDoDia.objects.filter(atividade_id=meta.atividade_id).aggregate(total_horas=Sum('horas_feitas'))
        meta.horas_semana = meta.horas_semana['total_horas'] or 0.0
        meta.percentual = 0 if meta.meta_horas == 0 else min(
            int((meta.horas_semana / meta.meta_horas) * 100),
            100
        )
            
    context = {
        "metas": metas,
        "dias_horas": dias_horas,
        "atividades": atividades,
        "atividades_vinculadas": atividades_vinculadas,
        "dias_vazios": dias_vazios,
    }
    
    return render(request,"home/index.html", context)

# View para criar/deletar atividade
def gerenciar_atividade(request):
    # Se for deletar atividades
    if request.method == "DELETE":
        data = json.loads(request.body)

        atividade_id = data.get("atividade_id")
        
        try:
            atividade = Atividade.objects.get(id=atividade_id)
            print(atividade.atividade.nome)
            atividade.delete()
            return JsonResponse({"status": "ok"}, status=200)
        except Atividade.DoesNotExist:
            return JsonResponse({"erro": "Atividade não encontrada"}, status=404)
    
    # Se for adicionar atividades
    if request.method == "POST":
        data = json.loads(request.body)
        
        # Operacao de criar atividade
        atividade = Atividade.objects.create(
            nome=data["nome_atividade"],
        )
        return JsonResponse({"id": atividade.id, "status": "ok"})
        
    return JsonResponse({"erro": "Metodo nao permitido"}, status=405)


def associar_atividade(request):
    # Se for adicionar atividades
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            print(f'Sacanagem: {data["nome_atividade"]}')
            atividade = Atividade.objects.get(nome=data["nome_atividade"])
            
            # Operacao de associar atividade
            novo_vinculo = AtividadeDoDia.objects.create(
                dia_semana=data["dia_semana"],
                horas_feitas= float (data["horas_feitas"]),
                atividade=atividade
            )
            
            soma_diaria = AtividadeDoDia.objects.filter(dia_semana=data["dia_semana"]).aggregate(total_horas=Sum('horas_feitas'))
            
            return JsonResponse({"status": "ok", "id": novo_vinculo.id, "soma_diaria": soma_diaria["total_horas"]})
        except Exception as e:
            print(f'erro? {e}')
            return JsonResponse({"erro": str(e)}, status=400)
    
    # Se for deletar atividades
    if request.method == "DELETE":
        data = json.loads(request.body)

        atividade_id = data.get("atividade_id")
        
        try:
            atividade = AtividadeDoDia.objects.get(id=atividade_id)
            atividade_nome = atividade.atividade.nome
            print(atividade.atividade.nome)
            dia = atividade.dia_semana
            atividade.delete()
            
            # Obtendo a soma diaria
            soma_diaria = AtividadeDoDia.objects.filter(dia_semana=dia).aggregate(total_horas=Coalesce(Sum('horas_feitas'), Value(0.0)))
            soma_diaria = soma_diaria["total_horas"]

            # Obtendo as horas investidas na meta da atividade deletada
            horas_da_meta = AtividadeDoDia.objects.filter(atividade_id=atividade_id).aggregate(total_horas=Sum('horas_feitas'))
            # Obtendo o numero
            horas_da_meta = horas_da_meta["total_horas"] or 0
            
            meta = Meta.objects.get(atividade__nome=atividade_nome)
            
            percentual = 0 if horas_da_meta == 0 else min(int((horas_da_meta / meta.meta_horas) * 100),100)
            
            context = {
                "dia": dia, 
                "id_meta": meta.id,
                "status": "ok", 
                "soma_diaria": soma_diaria, 
                "horas_da_meta": horas_da_meta,
                "percentual": percentual
            }
            
            return JsonResponse(context, status=200)
        except Atividade.DoesNotExist:
            return JsonResponse({"erro": "Atividade não encontrada"}, status=404)
        
    return JsonResponse({"erro": "Metodo nao permitido"}, status=405)


def metas(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            if data["operacao"] == "adicionar":
                atividade = Atividade.objects.get(nome=data["nome_atividade"])
                Meta.objects.create(
                    atividade = atividade,
                    meta_horas= float(data["meta_horas"])
                )
                return JsonResponse({"status": "ok"}, status=200)
            
            if data["operacao"] == "reset":
                meta = Meta.objects.get(nome=data["nome_atividade"])
                meta.meta_horas = 0
                meta.save()
                return JsonResponse({"status": "ok"}, status=200)
                
        except Exception as e:
            print(f'erro? {e}')
            return JsonResponse({"erro": str(e)}, status=400)

    
    atividades = Atividade.objects.all()
    metas = Meta.objects.all()

    for meta in metas:
        meta.horas_semana = AtividadeDoDia.objects.filter(atividade_id=meta.atividade_id).aggregate(total_horas=Sum('horas_feitas'))
        meta.horas_semana = meta.horas_semana['total_horas'] or 0.0
        meta.percentual = 0 if meta.meta_horas == 0 else min(
            int((meta.horas_semana / meta.meta_horas) * 100),
            100
        )
    
    metas_atingidas = sum(1 for meta in metas if meta.horas_semana >= meta.meta_horas)
    progresso_medio = round(sum(meta.percentual for meta in metas) / len(metas)) if metas else 0

    if progresso_medio >= 80:
        status = "Excelente!"
    elif progresso_medio >= 50:
        status = "No caminho certo"
    else:
        status = "Precisa melhorar"

    return render(request, "home/metas.html", {
        "atividades" : atividades,
        "metas": metas,
        "metas_atingidas": metas_atingidas,
        "total_metas": len(metas),
        "progresso_medio": progresso_medio,
        "status": status,
    })

def relatorios(request):
    soma_horas_semana = AtividadeDoDia.objects.aggregate(total_horas=Coalesce(Sum('horas_feitas'), Value(0.0)))
    
    dias_ativos = AtividadeDoDia.objects.values('dia_semana').distinct().count()
    
    soma_metas = Meta.objects.aggregate(total_horas=Coalesce(Sum('meta_horas'), Value(0.0)))
    
    percentual = (soma_horas_semana["total_horas"]/soma_metas["total_horas"]) * 100
    
    context =  {
        "soma_horas_semana": soma_horas_semana["total_horas"], 
        "soma_metas":soma_metas["total_horas"], 
        "dias_ativos": dias_ativos,
        "percentual": percentual
    }
        
    return render(request,"home/relatorios.html", context)

def hoje(request):
    return render(request, "home/hoje.html")

def calendario(request):
    return render(request, "home/calendario.html")

def atividades(request):
    # Obtendo todas as atividades do banco de dados
    atividades = Atividade.objects.all()
    
    
    return render(request, "home/atividades.html", {"atividades":atividades})