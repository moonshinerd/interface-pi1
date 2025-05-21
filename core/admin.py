from django.contrib import admin
from .models import Lancamento, Telemetria

@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    list_display = ('id_lancamento', 'data_hora_inicio', 'data_hora_fim')
    search_fields = ('id_lancamento',)
    list_filter = ('data_hora_inicio',)

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
        'latitude',
        'longitude',
        'altitude',
        'vel_sob_solo',
        'shunt_voltage',
        'bus_voltage',
        'current_mA',
        'power_mW',
    )
    search_fields = ('lancamento__id_lancamento', 'data_hora')
    list_filter = ('data_hora',)
