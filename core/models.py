from django.db import models

class Lancamento(models.Model):
    id_lancamento = models.AutoField(primary_key=True)
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField()

    volume_agua = models.FloatField(default=750.0, verbose_name="Volume de Água (mL)")
    angulo = models.FloatField(default=45.0, verbose_name="Ângulo (graus)")
    pressao_lancamento = models.FloatField(default=53.03, verbose_name="Pressão Recomendada (PSI)")

    DISTANCIA_CHOICES = [
        (10.0, '10 m'),
        (20.0, '20 m'),
        (30.0, '30 m'),
    ]
    distancia_alvo = models.FloatField(choices=DISTANCIA_CHOICES, default=10.0, verbose_name="Distância Alvo")

    def __str__(self):
        return f"Lançamento {self.id_lancamento}"

class Telemetria(models.Model):
    lancamento = models.ForeignKey(
        Lancamento,
        on_delete=models.CASCADE,
        related_name='telemetrias'
    )
    data_hora = models.DateTimeField()
    aceleracao_x = models.FloatField()
    aceleracao_y = models.FloatField()
    aceleracao_z = models.FloatField()
    vel_angular_x = models.FloatField()
    vel_angular_y = models.FloatField()
    vel_angular_z = models.FloatField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    altitude = models.FloatField(null=True, blank=True)
    vel_sob_solo = models.FloatField(null=True, blank=True)
    shunt_voltage = models.FloatField(null=True, blank=True)
    bus_voltage = models.FloatField(null=True, blank=True)
    current_mA = models.FloatField(null=True, blank=True)
    power_mW = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['data_hora']

    def __str__(self):
        return f"Telemetria {self.pk} @ {self.data_hora}"
