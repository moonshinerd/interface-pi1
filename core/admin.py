from django.contrib import admin
from .models import Lancamento, Telemetria

@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    list_display = (
        'id_lancamento',
        'data_hora_inicio',
        'data_hora_fim',
        'distancia_alvo',
        'volume_agua',
        'angulo',
        'pressao_lancamento',
    )
    search_fields = ('id_lancamento',)
    list_filter = ('data_hora_inicio',)
    readonly_fields = ('volume_agua', 'angulo', 'pressao_lancamento')


@admin.register(Telemetria)
class TelemetriaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'lancamento',
        'data_hora',
        'aceleracao_x',
        'aceleracao_y',
        'aceleracao_z',
        'vel_angular_x',
        'vel_angular_y',
        'vel_angular_z',
        'temperatura',
        'latitude',
        'longitude',
        'altitude',
        'velocidade',
    )
    search_fields = (
        'lancamento__id_lancamento',
        'data_hora',
    )
    list_filter = ('data_hora',)
    # Se quiser deixar algum campo somente leitura, adicione em readonly_fields
    # readonly_fields = ('temperatura',)
