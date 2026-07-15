from django.contrib import admin
from .models import Atividade, AtividadeDoDia, Meta

admin.site.register(Atividade)
admin.site.register(AtividadeDoDia)
admin.site.register(Meta)