from django.test import TestCase
from core.models import Lancamento, Telemetria
from django.utils import timezone
from core.utils import (
    criar_figura_aceleracao_x_tempo,
    criar_figura_gps_3d,
    criar_figura_tensao_potencia,
    criar_figura_gps_mapa,
    criar_figura_velocidade_angular
)
import plotly.graph_objects as go

class OldLaunchesViewTest(TestCase):
    def setUp(self):
        now = timezone.now()
        self.lancamento1 = Lancamento.objects.create(
            data_hora_inicio=now,
            data_hora_fim=now,
            volume_agua=100,
            angulo=45,
            pressao_lancamento=30,
            distancia_alvo=10,
        )
        self.lancamento2 = Lancamento.objects.create(
            data_hora_inicio=now,
            data_hora_fim=now,
            volume_agua=150,
            angulo=60,
            pressao_lancamento=40,
            distancia_alvo=20,
        )

    def test_oldlaunches_table_contains_lancamentos(self):
        response = self.client.get('/oldlaunches/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn(str(self.lancamento1), content)
        self.assertIn(str(self.lancamento2), content)

class LancamentoModelTest(TestCase):
    def test_criar_lancamento_valido(self):
        lancamento = Lancamento.objects.create(
            data_hora_inicio=timezone.now(),
            data_hora_fim=timezone.now(),
            volume_agua=750.0,
            angulo=45.0,
            pressao_lancamento=53.03,
            distancia_alvo=10.0
        )
        self.assertIsNotNone(lancamento.id_lancamento)
        self.assertEqual(lancamento.volume_agua, 750.0)
        self.assertEqual(lancamento.angulo, 45.0)

    def test_distancia_alvo_choices(self):
        lancamento = Lancamento.objects.create(
            data_hora_inicio=timezone.now(),
            data_hora_fim=timezone.now(),
            distancia_alvo=20.0
        )
        self.assertIn(lancamento.distancia_alvo, [10.0, 20.0, 30.0])

