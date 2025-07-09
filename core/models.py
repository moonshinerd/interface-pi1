from django.db import models

class Lancamento(models.Model):
    id_lancamento = models.AutoField(primary_key=True)
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField(null=True, blank=True, help_text="Deixe em branco para lançamentos ativos")

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

    @property
    def esta_ativo(self):
        """Retorna True se o lançamento está ativo (sem data_hora_fim)"""
        return self.data_hora_fim is None

class Telemetria(models.Model):
    lancamento = models.ForeignKey(
        Lancamento,
        on_delete=models.CASCADE,
        related_name='telemetrias'
    )
    data_hora = models.DateTimeField(help_text="Data e hora completa do registro de telemetria")

    # Acelerações (g)
    aceleracao_x = models.FloatField(verbose_name="Aceleração X (g)")
    aceleracao_y = models.FloatField(verbose_name="Aceleração Y (g)")
    aceleracao_z = models.FloatField(verbose_name="Aceleração Z (g)")

    # Velocidades angulares (°/s)
    vel_angular_x = models.FloatField(verbose_name="Giro X (°/s)")
    vel_angular_y = models.FloatField(verbose_name="Giro Y (°/s)")
    vel_angular_z = models.FloatField(verbose_name="Giro Z (°/s)")

    # Temperatura (°C)
    temperatura = models.FloatField(verbose_name="Temperatura (°C)")

    # Dados de GPS
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    altitude = models.FloatField(null=True, blank=True)

    # Velocidade sobre o solo (km/h)
    velocidade = models.FloatField(null=True, blank=True, verbose_name="Velocidade (km/h)")

    class Meta:
        ordering = ['data_hora']

    def __str__(self):
        return f"Telemetria {self.pk} @ {self.data_hora}"
