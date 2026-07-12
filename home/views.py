from multiprocessing import context

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.utils import timezone
from .models import Atividade, Meta, AtividadeDoDia
import json
from collections import defaultdict
from django.contrib.auth.decorators import login_required


# Lista de dias da semana, usada para manter a ordem correta na exibicao dos dados
DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

<<<<<<< Updated upstream
=======
# Funcao auxiliar que retorna a data de hoje formatada, usada em varias views
def data_formatada():
    hoje_data = timezone.localdate()
    dia_semana_hoje = DIAS[hoje_data.weekday()] 

    dias_extenso = {
        "Segunda": "Segunda-feira",
        "Terça": "Terça-feira",
        "Quarta": "Quarta-feira",
        "Quinta": "Quinta-feira",
        "Sexta": "Sexta-feira",
        "Sábado": "Sábado",
        "Domingo": "Domingo",
    }
    meses = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    data_formatada = f"{dias_extenso[dia_semana_hoje]}, {hoje_data.day} de {meses[hoje_data.month]} de {hoje_data.year}"
    
    return data_formatada

@login_required
>>>>>>> Stashed changes
def index(request):
    # Obtendo todas as atividades do banco de dados e os vinculos
    atividades  = Atividade.objects.prefetch_related('vinculos_dias').all()
    vinculos    = AtividadeDoDia.objects.all()
    
    # Obtendo os dias que possuem alguma atividade
    dias_usados = AtividadeDoDia.objects.values_list("dia_semana",flat=True).distinct()
    dias_vazios = list(set(DIAS)  - set(dias_usados))
    
    # Criando um dicionario para colocar a soma total diaria de cada atividade
    soma_por_dia = defaultdict(float)
    for atividade in vinculos:
        # Cada posicao do dicionario é um dia da semana. Somamos nesse dia a quantidade de horas investidas na atividade da iteracao
        soma_por_dia[atividade.dia_semana] += atividade.horas_feitas
      
    # Criando uma lista que contem, na mesma ordem da lista "DIAS", o total de horas trabalhadas em cada um dos dias
    total_horas_por_dia = [soma_por_dia[dia] for dia in DIAS]
    
    # dias_horas é a variavel que possui uma lista de tuplas, em que cada elemento é um dia seguido 
    # das horas trabalhadas nele (somando todas as atividades)
    dias_horas = zip(DIAS, total_horas_por_dia)
    
    metas, _ = gerar_estatisticas_metas()

    hoje_data = timezone.localdate()
    dia_semana_hoje = dias[hoje_data.weekday()]  # a lista "dias" já existe lá em cima do arquivo

    dias_extenso = {
        "Segunda": "Segunda-feira",
        "Terça": "Terça-feira",
        "Quarta": "Quarta-feira",
        "Quinta": "Quinta-feira",
        "Sexta": "Sexta-feira",
        "Sábado": "Sábado",
        "Domingo": "Domingo",
    }
    meses = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    data_formatada = f"{dias_extenso[dia_semana_hoje]}, {hoje_data.day} de {meses[hoje_data.month]} de {hoje_data.year}"
            
    context = {
        "data_formatada": data_formatada,
        "metas": metas,
        "dias_horas": dias_horas,
        "atividades": atividades,
        "vinculos": vinculos,
        "dias_vazios": dias_vazios,
    }
    
    return render(request,"home/index.html", context)

# View para criar/deletar atividade
def gerenciar_atividade(request):
    data = json.loads(request.body)

    # Se for deletar atividades
    if request.method == "DELETE":
        # Obtendo o id da atividade passado via json
        atividade_id = data.get("atividade_id")
        try:
            # Obtem o objeto da atividade
            atividade = Atividade.objects.get(id=atividade_id)
            print(f'Atividade deletada: {atividade.nome}')
            atividade.delete()
            return JsonResponse({"status": "ok"}, status=200)
        except Exception as e:
            print(f'erro? {e}')
            return JsonResponse({"erro": str(e)}, status=400)
    
    # Se for adicionar atividades
    if request.method == "POST":
        try:
            # Cria uma atividade nova e retorna o id
            atividade = Atividade.objects.create(
                nome=data["nome_atividade"],
            )
            return JsonResponse({"id": atividade.id}, status=200)
        except Exception as e:
            print(f'erro? {e}')
            return JsonResponse({"erro": str(e)}, status=400)
        
    return JsonResponse({"erro": "Metodo nao permitido"}, status=405)

# View que retorna a pagina de atividades
def atividades(request):
    # Obtendo todas as atividades do banco de dados
    atividades = Atividade.objects.all()
    
    # Retorna as atividades e a pagina html
    return render(request, "home/atividades.html", {"atividades":atividades})

# Funcao auxiliar para obter as informacoes importantes da atividade vinculada ao dia da semana
def gerar_dados_atividade(dia, atividade_nome, id=None, operacao=None):
    # Obtendo a soma diaria (usado para atualizar total de horas do dia)
    consulta_soma_diaria = AtividadeDoDia.objects.filter(dia_semana=dia).aggregate(total_horas=Coalesce(Sum('horas_feitas'), Value(0.0)))
    # Obtendo o valor retornado dentro do dicionario
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
    context = {
        "dia": dia, 
        "soma_diaria": soma_diaria, 
        "horas_da_meta": horas_da_meta,
    }
    
    # Se a operação for de adição, passa o id do novo vinculo
    if operacao == "adicionar" and id is not None:
        context["id"] = id  
    
    # Caso a meta exista, preenche os campos da meta
    if meta is not None:
        percentual = 0 if horas_da_meta == 0 else min(int((horas_da_meta / meta.meta_horas) * 100),100)
        context["id_meta"] = meta.id
        context["percentual"] = percentual

    # Caso nao exista, preenche os campos da meta com vazio
    else:                
        context["id_meta"] = "None"
        context["percentual"] = "None"
    
    return context    

def atualizar_horas(request):
    data = json.loads(request.body)
    if request.method == "POST":
        try:
            novo_valor = data["horas_feitas"]

            vinculo = AtividadeDoDia.objects.get(id=data["vinculo_id"])
            vinculo.horas_feitas = novo_valor
            vinculo.save()

            print(f'Atualizado horas da atividade {vinculo.atividade.nome} no dia {vinculo.dia_semana} para {novo_valor}')
    
            context = gerar_dados_atividade(vinculo.dia_semana, vinculo.atividade.nome)
            return JsonResponse(context, status=200)
        except Exception as e:
            print(f'erro? {e}')
            return JsonResponse({"erro": str(e)}, status=400)

# View para associar uma atividade a um dia da semana
def associar_atividade(request):
    # Obtem os dados passados pelo front
    data = json.loads(request.body)

    # Se for adicionar atividades
    if request.method == "POST":
        try:
            print(f'Atividade a ser associada: {data["nome_atividade"]}')
            atividade = Atividade.objects.get(nome=data["nome_atividade"])
            
            # Operacao de associar atividade
            novo_vinculo = AtividadeDoDia.objects.create(
                dia_semana=data["dia_semana"],
                horas_feitas= float (data["horas_feitas"]),
                atividade=atividade
            )
            
            # Se foi enviada uma meta semanal e a atividade ainda nao tem meta, cria automaticamente
            meta_horas_recebida = data.get("meta_horas")
            if meta_horas_recebida:
                ja_tem_meta = Meta.objects.filter(atividade=atividade).exists()
                if not ja_tem_meta:
                    Meta.objects.create(
                        atividade=atividade,
                        meta_horas=float(meta_horas_recebida)
                    )
            
            # Obtem o contexto pela funcao auxiliar
            context = gerar_dados_atividade(data["dia_semana"], atividade.nome, novo_vinculo.id, operacao="adicionar")
            
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
            atividade_nome = vinculo.atividade.nome
            dia = vinculo.dia_semana
            
            # Deleta o vinculo do banco
            vinculo.delete()
            
            # Obtem o contexto pela funcao auxiliar
            context = gerar_dados_atividade(dia, atividade_nome)
            return JsonResponse(context, status=200)

        except Exception as e:
            print(f'erro? {e}')
            return JsonResponse({"erro": str(e)}, status=400)
        
    return JsonResponse({"erro": "Metodo nao permitido"}, status=405)

# Funcao auxiliar para gerar estatisticas das metas. O parametro nome_atividade é opcional, e caso seja passado, a funcao retorna 
def gerar_estatisticas_metas(nome_atividade=None):
    # Cria uma variavel para a nova meta, caso seja necessario usá-la no retorno da funcao
    novameta = None
    # Itera sobre as metas, calculando o total de horas trabalhadas em todas as atividades e obtendo o percentual com relacao a meta estabelecida
    metas = Meta.objects.all()
    for meta in metas:
        # Realiza uma consulta que retorna a soma de todas as horas feitas na atividade vinculada à meta
        consulta_HorasMeta_semana = AtividadeDoDia.objects.filter(atividade_id=meta.atividade_id).aggregate(total_horas=Sum('horas_feitas'))
        # Obtem o valor retornado dentro do dicionario, e caso nao haja nenhuma hora feita, retorna 0.0
        meta.horas_semana = consulta_HorasMeta_semana['total_horas'] or 0.0
        # Faz o calculo do percentual de horas feitas em relacao a meta estabelecida, limitando o valor a 100%
        meta.percentual = 0 if meta.meta_horas == 0 else min(
            int((meta.horas_semana / meta.meta_horas) * 100),
            100
        )
        # Se foi passado o nome da atividade, passa a novameta
        if nome_atividade == meta.atividade.nome:
            novameta = meta
    
    # Retorna a lista de metas com dados de horas da semana e a nova meta, caso tenha sido passada uma atividade
    return (metas, novameta)

# Funcao auxiliar para obter as informacoes importantes da meta
def gerar_dados_metas(nome_atividade=None, operacao=None):        
    # Gera as estatisticas das metas, e caso seja passada uma atividade, tambem retorna a meta vinculada a ela
    metas, novameta = gerar_estatisticas_metas(nome_atividade=nome_atividade)
    
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

    
    hoje_data = timezone.localdate()
    dia_semana_hoje = dias[hoje_data.weekday()]  # a lista "dias" já existe lá em cima do arquivo

    dias_extenso = {
        "Segunda": "Segunda-feira",
        "Terça": "Terça-feira",
        "Quarta": "Quarta-feira",
        "Quinta": "Quinta-feira",
        "Sexta": "Sexta-feira",
        "Sábado": "Sábado",
        "Domingo": "Domingo",
    }
    meses = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    data_formatada = f"{dias_extenso[dia_semana_hoje]}, {hoje_data.day} de {meses[hoje_data.month]} de {hoje_data.year}"

    # Monta o contexto
    context = {
        "data_formatada": data_formatada,
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
            
            # Se a operacao for de adição, obtem a atividade associada e cria uma nova meta. Retorna os dados para atualizar o front
            if data["operacao"] == "adicionar":
                atividade = Atividade.objects.get(nome=data["nome_atividade"])
                Meta.objects.create(
                    atividade = atividade,
                    meta_horas= float(data["meta_horas"])
                )
                # Obtem o contexto
                context = gerar_dados_metas(nome_atividade=atividade.nome, operacao="adicionar")
                return JsonResponse(context, status=200)
            
                # Se a operacao for de deleção, obtem a meta com o nome da atividade, deleta e retorna os dados para atualizar o front
            if data["operacao"] == "deletar":
                meta = Meta.objects.get(atividade__nome=data["nome_atividade"])
                meta.delete()
                context = gerar_dados_metas(operacao="deletar")
                return JsonResponse(context, status=200)
        
        # Caso houve alguma exception, retorna o erro para o front
        except Exception as e:
            print(f'erro? {e}')
            return JsonResponse({"erro": str(e)}, status=400)

    # Caso seja apenas para carregar a pagina, gera o contexto com todas as metas e retorna a pagina
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
        
    horas_por_dia_consulta = AtividadeDoDia.objects.values('dia_semana').annotate(
        total=Coalesce(Sum('horas_feitas'), Value(0.0))
    )
    horas_map = {item['dia_semana']: item['total'] for item in horas_por_dia_consulta}

    # Garante que todos os dias aparecem, mesmo os sem atividade
    horas_por_dia = [horas_map.get(dia, 0.0) for dia in DIAS]
    
    hoje_data = timezone.localdate()
    dia_semana_hoje = dias[hoje_data.weekday()]  # a lista "dias" já existe lá em cima do arquivo

    dias_extenso = {
        "Segunda": "Segunda-feira",
        "Terça": "Terça-feira",
        "Quarta": "Quarta-feira",
        "Quinta": "Quinta-feira",
        "Sexta": "Sexta-feira",
        "Sábado": "Sábado",
        "Domingo": "Domingo",
    }
    meses = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    data_formatada = f"{dias_extenso[dia_semana_hoje]}, {hoje_data.day} de {meses[hoje_data.month]} de {hoje_data.year}"
    top5 = AtividadeDoDia.objects.values('atividade__nome') \
                                       .annotate(total_horas=Sum('horas_feitas')) \
                                       .filter(total_horas__gt=0) \
                                       .order_by('-total_horas')[:5]

    context =  {
        "data_formatada": data_formatada,
        "soma_horas_semana": soma_horas_semana["total_horas"], 
        "soma_metas":soma_metas["total_horas"], 
        "top5": top5,
        "dias_ativos": dias_ativos,
        "eficiencia": eficiencia,
        "grafico_labels": DIAS,
        "grafico_dados": horas_por_dia,
    }
        
    return render(request,"home/relatorios.html", context)


def hoje(request):
    hoje_data = timezone.localdate()
    dia_semana_hoje = dias[hoje_data.weekday()]  # a lista "dias" já existe lá em cima do arquivo

    dias_extenso = {
        "Segunda": "Segunda-feira",
        "Terça": "Terça-feira",
        "Quarta": "Quarta-feira",
        "Quinta": "Quinta-feira",
        "Sexta": "Sexta-feira",
        "Sábado": "Sábado",
        "Domingo": "Domingo",
    }
    meses = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    data_formatada = f"{dias_extenso[dia_semana_hoje]}, {hoje_data.day} de {meses[hoje_data.month]} de {hoje_data.year}"

    vinculos_hoje = AtividadeDoDia.objects.filter(dia_semana=dia_semana_hoje).select_related('atividade')

    atividades_hoje = []
    soma_horas_feitas = 0.0
    soma_metas_diarias = 0.0
    total_concluidas = 0

    for vinculo in vinculos_hoje:
        # Quantos dias da semana essa atividade aparece (pra dividir a meta semanal entre eles)
        dias_cadastrados = AtividadeDoDia.objects.filter(atividade=vinculo.atividade).count()

        # Busca a meta semanal da atividade, se existir
        meta = Meta.objects.filter(atividade=vinculo.atividade).first()

        if meta and dias_cadastrados > 0:
            meta_diaria = meta.meta_horas / dias_cadastrados
        else:
            meta_diaria = 0.0

        if meta_diaria == 0:
            percentual = 0
        else:
            percentual = min(int((vinculo.horas_feitas / meta_diaria) * 100), 100)
        
        concluida = percentual >= 100

        if concluida:
            total_concluidas += 1

        soma_horas_feitas += vinculo.horas_feitas
        soma_metas_diarias += meta_diaria

        atividades_hoje.append({
            "id": vinculo.id,
            "nome": vinculo.atividade.nome,
            "horas_feitas": vinculo.horas_feitas,
            "meta_diaria": round(meta_diaria, 1),
            "percentual": percentual,
            "concluida": concluida,
        })

    if soma_metas_diarias == 0:
        progresso_geral = 0 
    else:
        progresso_geral = min(int((soma_horas_feitas / soma_metas_diarias) * 100), 100)

    context = {
        "data_formatada": data_formatada,
        "atividades_hoje": atividades_hoje,
        "soma_horas_feitas": round(soma_horas_feitas, 1),
        "soma_metas_diarias": round(soma_metas_diarias, 1),
        "total_concluidas": total_concluidas,
        "total_atividades_hoje": len(atividades_hoje),
        "progresso_geral": progresso_geral,
    }

    return render(request, "home/hoje.html", context)


# View nova, pra atualizar as horas feitas de uma atividade específica hoje
def atualizar_horas_hoje(request):
    # print(request.POST)
    if request.method == "POST":
        vinculo_id = request.POST.get("vinculo_id")
        horas_feitas = request.POST.get("horas_feitas")

        try:
            vinculo = AtividadeDoDia.objects.get(id=vinculo_id)
            vinculo.horas_feitas = float(horas_feitas)
            vinculo.save()
        except AtividadeDoDia.DoesNotExist:
            pass  # se o vinculo nao existir mais, so ignora e volta pra tela

    return redirect('hoje')


# View para a pagina do dia de hoje
def calendario(request):
    return render(request, "home/calendario.html")