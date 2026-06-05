from django.db import models

# Create your models here.

class Mensagem(models.Model):
    titulo = models.CharField(max_length=120)
    conteudo = models.TextField()
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criada_em"]

    def __str__(self):
        return self.titulo
    
class Atividade(models.Model):
    nome = models.CharField(max_length=200)
    dia_semana = models.CharField(max_length=20)
    # horas = models.

    def __str__(self):
        return self.nome