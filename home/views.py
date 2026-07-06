from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from .models import Atividade, Meta, AtividadeDoDia
import json
from collections import defaultdict

dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

def index(request):
    # Obtendo todas as atividades do banco de dados e os vinculos
    atividades  = Atividade.objects.prefetch_related('vinculos_dias').all()
    vinculos    = AtividadeDoDia.objects.all()
    
    # Obtendo os dias que possuem alguma atividade
    dias_usados = AtividadeDoDia.objects.values_list("dia_semana",flat=True).distinct()
    dias_vazios = list(set(dias)  - set(dias_usados))
    
    # Criando um dicionario para colocar a soma total diaria de cada atividade
    soma_por_dia = defaultdict(float)
    for atividade in vinculos:
        # Cada posicao do dicionario é um dia da semana. Somamos nesse dia a quantidade de horas investidas na atividade da iteracao
        soma_por_dia[atividade.dia_semana] += atividade.horas_feitas
      
    # Criando uma lista que contem, na mesma ordem da lista "dias", o total de horas trabalhadas em cada um dos dias
    total_horas_por_dia = [soma_por_dia[dia] for dia in dias]
    
    # dias_horas é a variavel que possui uma lista de tuplas, em que cada elemento é um dia seguido 
    # das horas trabalhadas nele (somando todas as atividades)
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
        "vinculos": vinculos,
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
            print(f'Atividade deletada: {atividade.nome}')
            atividade.delete()
            return JsonResponse({"status": "ok"}, status=200)
        except Atividade.DoesNotExist:
            return JsonResponse({"erro": "Atividade não encontrada"}, status=404)
    
    # Se for adicionar atividades
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            # Operacao de criar atividade
            atividade = Atividade.objects.create(
                nome=data["nome_atividade"],
            )
            return JsonResponse({"id": atividade.id, "status": "ok"})
        except Exception as e:
            print(f'erro? {e}')
            return JsonResponse({"erro": str(e)}, status=400)
        
    return JsonResponse({"erro": "Metodo nao permitido"}, status=405)

# View para o gerenciamento de atividades cadastradas
def atividades(request):
    # Obtendo todas as atividades do banco de dados
    atividades = Atividade.objects.all()
    
    # Retorna as atividades e a pagina html
    return render(request, "home/atividades.html", {"atividades":atividades})

# View para associar uma atividade a um dia da semana
def associar_atividade(request):
    # Obtem os dados passados pelo front
    data = json.loads(request.body)

    # Se for adicionar atividades
    if request.method == "POST":
        try:
            print(f'Atividade: {data["nome_atividade"]}')
            atividade = Atividade.objects.get(nome=data["nome_atividade"])
            
            # Operacao de associar atividade
            novo_vinculo = AtividadeDoDia.objects.create(
                dia_semana=data["dia_semana"],
                horas_feitas= float (data["horas_feitas"]),
                atividade=atividade
            )
            
            # Salva o dia
            dia = data["dia_semana"]
            
            # Obtendo a soma diaria (usado para atualizar total de horas do dia)
            consulta_soma_diaria = AtividadeDoDia.objects.filter(dia_semana=dia).aggregate(total_horas=Coalesce(Sum('horas_feitas'), Value(0.0)))
            soma_diaria = consulta_soma_diaria["total_horas"]

            # Obtendo as horas investidas na meta da atividade 
            consulta_horas_da_meta = AtividadeDoDia.objects.filter(atividade_id=atividade.id).aggregate(total_horas=Sum('horas_feitas'))
            # Obtendo o valor retornado dentro do dicionario
            horas_da_meta = consulta_horas_da_meta["total_horas"] or 0
            
            # Tenta buscar uma meta existente vinculada à atividade. Se nao achar, retorna None
            try:
                meta = Meta.objects.get(atividade__nome=atividade.nome)
            except Meta.DoesNotExist:
                meta = None
            
            # Caso exista a meta, passa as infromacoes e calcula o percentual
            if meta != None:
                percentual = 0 if horas_da_meta == 0 else min(int((horas_da_meta / meta.meta_horas) * 100),100)
                context = {
                    "id": novo_vinculo.id, 
                    "dia": dia, 
                    "soma_diaria": soma_diaria, 
                    "horas_da_meta": horas_da_meta,
                    "id_meta": meta.id,
                    "percentual": percentual,
                }
            # Caso nao exista, preenche os campos da meta com vazio
            else:                
                context = {
                    "id": novo_vinculo.id, 
                    "dia": dia, 
                    "soma_diaria": soma_diaria, 
                    "horas_da_meta": horas_da_meta,
                    "id_meta": "None",
                    "percentual": "None"
                }   
            
            return JsonResponse(context, status=200)
        except Exception as e:
            print(f'erro? {e}')
            return JsonResponse({"erro": str(e)}, status=400)
    
    # Se for deletar atividades
    if request.method == "DELETE":
        # Obtendo o id da atividade passado via json
        id_vinculo = data.get("vinculo_id")
        
        try:
            # Obtendo o objeto da atividade
            vinculo = AtividadeDoDia.objects.get(id=id_vinculo)
            # Salva o nome e o dia
            atividade_nome = vinculo.atividade.nome
            dia = vinculo.dia_semana
            # Deleta do banco
            vinculo.delete()
            
            # Obtendo a soma diaria (usado para atualizar total de horas do dia)
            consulta_soma_diaria = AtividadeDoDia.objects.filter(dia_semana=dia).aggregate(total_horas=Coalesce(Sum('horas_feitas'), Value(0.0)))
            soma_diaria = consulta_soma_diaria["total_horas"]

            # Obtendo as horas investidas na meta da atividade deletada
            consulta_horas_da_meta = AtividadeDoDia.objects.filter(atividade__nome=atividade_nome).aggregate(total_horas=Sum('horas_feitas'))
            # Obtendo o valor retornado dentro do dicionario
            horas_da_meta = consulta_horas_da_meta["total_horas"] or 0
            
            # Tenta buscar uma meta existente vinculada à atividade deletada. Se nao achar, retorna None
            try:
                meta = Meta.objects.get(atividade__nome=atividade_nome)
            except Meta.DoesNotExist:
                meta = None
            
            # Caso exista a meta, passa as infromacoes e calcula o percentual
            if meta != None:
                percentual = 0 if horas_da_meta == 0 else min(int((horas_da_meta / meta.meta_horas) * 100),100)
                context = {
                    "dia": dia, 
                    "id_meta": meta.id,
                    "status": "ok", 
                    "soma_diaria": soma_diaria, 
                    "horas_da_meta": horas_da_meta,
                    "percentual": percentual
                }
            # Caso nao exista, preenche os campos da meta com vazio
            else:                
                context = {
                    "dia": dia, 
                    "id_meta": "None",
                    "status": "ok", 
                    "soma_diaria": soma_diaria, 
                    "horas_da_meta": horas_da_meta,
                    "percentual": "None"
                }   
            
            return JsonResponse(context, status=200)
        except Atividade.DoesNotExist:
            return JsonResponse({"erro": "Atividade não encontrada"}, status=404)
        
    return JsonResponse({"erro": "Metodo nao permitido"}, status=405)

# Funcao auxiliar para obter as informacoes importantes da meta
def gerar_dados_metas(nome_atividade=None, operacao=None):        
    # Itera sobre as metas, calculando o total de horas trabalhadas em todas as atividades e obtendo o percentual com relacao a meta estabelecida
    metas = Meta.objects.all()
    for meta in metas:
        meta.horas_semana = AtividadeDoDia.objects.filter(atividade_id=meta.atividade_id).aggregate(total_horas=Sum('horas_feitas'))
        meta.horas_semana = meta.horas_semana['total_horas'] or 0.0
        meta.percentual = 0 if meta.meta_horas == 0 else min(
            int((meta.horas_semana / meta.meta_horas) * 100),
            100
        )
        # Se foi passado o nome da atividade, procura a meta correspondente e salva em novameta
        if nome_atividade == meta.atividade.nome:
            novameta = meta
    
    # Calculo das metas atingidas para a semana
    metas_atingidas = sum(1 for meta in metas if meta.horas_semana >= meta.meta_horas)
    # Calculo do progesso medio em percentual
    progresso_medio = round(sum(meta.percentual for meta in metas) / len(metas)) if metas else 0

    # Status do progresso
    if progresso_medio >= 80:
        status = "Excelente!"
    elif progresso_medio >= 50:
        status = "No caminho certo"
    else:
        status = "Precisa melhorar"

    # Se nao foi passada uma atividade, retorna todos os dados
    atividades_sem_meta = list(Atividade.objects.filter(vinculos_metas__isnull=True).values_list('nome', flat=True))
    print(f'Atividades sem meta: {atividades_sem_meta}')

    # Contexto da delecao -> o que carrega menos informacoes
    context = {
        "atividades" : atividades_sem_meta,
        "metas_atingidas": metas_atingidas,
        "total_metas": len(metas),
        "progresso_medio": progresso_medio,
        "status": status,
    }

    # Caso uma atividade tenha sido passada, adiciona tambem os dados especificos da meta nova
    if operacao == "adicionar" and nome_atividade is not None:
        context["horas_semana"] = novameta.horas_semana
        context["percentual"] = novameta.percentual

    # Caso nada tenha sido passado, é o retorno da view quando carrega a pagina, entao adiciona todas as metas
    if operacao == None:
        context["metas"] = metas
        
    return context


# View para as metas
def metas(request):
    # Se for criar uma meta nova
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            if data["operacao"] == "adicionar":
                atividade = Atividade.objects.get(nome=data["nome_atividade"])
                Meta.objects.create(
                    atividade = atividade,
                    meta_horas= float(data["meta_horas"])
                )
                context = gerar_dados_metas(nome_atividade=atividade.nome, operacao="adicionar")
                
                return JsonResponse(context, status=200)
            
            if data["operacao"] == "deletar":
                meta = Meta.objects.get(atividade__nome=data["nome_atividade"])
                meta.delete()
                context = gerar_dados_metas(operacao="deletar")
                return JsonResponse(context, status=200)
                
        except Exception as e:
            print(f'erro? {e}')
            return JsonResponse({"erro": str(e)}, status=400)

    context = gerar_dados_metas()
    return render(request, "home/metas.html", context)
    

# View para a exibicao dos relatorios
def relatorios(request):
    soma_horas_semana = AtividadeDoDia.objects.aggregate(total_horas=Coalesce(Sum('horas_feitas'), Value(0.0)))
    
    dias_ativos = AtividadeDoDia.objects.values('dia_semana').distinct().count()
    
    soma_metas = Meta.objects.aggregate(total_horas=Coalesce(Sum('meta_horas'), Value(0.0)))
    
    try:    
        eficiencia = (soma_horas_semana["total_horas"]/soma_metas["total_horas"]) * 100
    except ZeroDivisionError:
        eficiencia = 0
    
    context =  {
        "soma_horas_semana": soma_horas_semana["total_horas"], 
        "soma_metas":soma_metas["total_horas"], 
        "dias_ativos": dias_ativos,
        "eficiencia": eficiencia
    }
        
    return render(request,"home/relatorios.html", context)

# View para a pagina do dia de hoje
def hoje(request):
    return render(request, "home/hoje.html")

# View para a pagina do dia de hoje
def calendario(request):
    return render(request, "home/calendario.html")