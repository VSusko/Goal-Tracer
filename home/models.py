from django.db import models

   
class Atividade(models.Model):
    nome = models.CharField(max_length=200, unique=True) # unique=True evita nomes duplicados

    def __str__(self):
        return self.nome

class AtividadeDoDia(models.Model):
    DIAS_CHOICES = [
        ("Segunda", "Segunda"),
        ("Terça", "Terça"),
        ("Quarta", "Quarta"),
        ("Quinta", "Quinta"),
        ("Sexta", "Sexta"),
        ("Sábado", "Sábado"),
        ("Domingo", "Domingo"),
    ]
    semana = models.BigIntegerField(default=1)

    dia_semana = models.CharField(max_length=20, choices=DIAS_CHOICES)
    
    # Aponta para a atividade base cadastrada
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name="vinculos_dias")
    
    # Aqui ficam os dados específicos deste dia!
    horas_feitas = models.FloatField(default=0.0)
    
    class Meta:
        # Evita que a MESMA atividade seja adicionada duas vezes no MESMO dia da semana
        unique_together = ('dia_semana', 'atividade')

    def __str__(self):
        return f"{self.atividade.nome} na {self.get_dia_semana_display()}"    
    

class Meta(models.Model):
    semana = models.BigIntegerField(default=1)
    meta_horas = models.FloatField(default=0.0)
    
    # Aponta para a atividade base cadastrada
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name="vinculos_metas")


    def __str__(self):
        return self.nome