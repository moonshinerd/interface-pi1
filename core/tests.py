from django.test import TestCase
from core.models import Lancamento
from django.utils import timezone

class OldLaunchesViewTest(TestCase):
    def setUp(self):
        now = timezone.now()
        self.lancamento1 = Lancamento.objects.create(
            data_hora_inicio=now,
            data_hora_fim=now,
            volume_agua=100,
            angulo=45,
            pressao_ajustada=30,
            distancia_alvo=10,
        )
        self.lancamento2 = Lancamento.objects.create(
            data_hora_inicio=now,
            data_hora_fim=now,
            volume_agua=150,
            angulo=60,
            pressao_ajustada=40,
            distancia_alvo=20,
        )

    def test_oldlaunches_table_contains_lancamentos(self):
        response = self.client.get('/oldlaunches/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn(str(self.lancamento1), content)
        self.assertIn(str(self.lancamento2), content)
