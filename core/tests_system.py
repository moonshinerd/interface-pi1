from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from core.models import Lancamento, Telemetria
from core.utils import (
    criar_figura_aceleracao_x_tempo,
    criar_figura_gps_3d,
    criar_figura_tensao_potencia,
    criar_figura_gps_mapa,
    criar_figura_velocidade_angular
)

class SystemTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.lancamento = Lancamento.objects.create(
            data_hora_inicio=timezone.now(),
            data_hora_fim=timezone.now(),
            volume_agua=750.0,
            angulo=45.0,
            pressao_lancamento=53.03,
            distancia_alvo=10.0
        )

    def test_fluxo_completo_sistema(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

        response = self.client.get('/oldlaunches/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/launch_list.html')
        self.assertContains(response, str(self.lancamento))

        response = self.client.get(f'/oldlaunches/{self.lancamento.id_lancamento}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oldlaunches/detail.html')
        self.assertContains(response, str(self.lancamento.id_lancamento))

    def test_sistema_com_multiplos_lancamentos(self):
        """Testa o sistema com múltiplos lançamentos e suas interações"""
        lancamento2 = Lancamento.objects.create(
            data_hora_inicio=timezone.now(),
            data_hora_fim=timezone.now(),
            volume_agua=800.0,
            angulo=50.0,
            pressao_lancamento=55.0,
            distancia_alvo=12.0
        )
        
        lancamento3 = Lancamento.objects.create(
            data_hora_inicio=timezone.now(),
            data_hora_fim=timezone.now(),
            volume_agua=900.0,
            angulo=55.0,
            pressao_lancamento=60.0,
            distancia_alvo=15.0
        )

        response = self.client.get('/oldlaunches/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.lancamento))
        self.assertContains(response, str(lancamento2))
        self.assertContains(response, str(lancamento3))

        for lancamento in [self.lancamento, lancamento2, lancamento3]:
            response = self.client.get(f'/oldlaunches/{lancamento.id_lancamento}/')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'oldlaunches/detail.html')
            self.assertContains(response, str(lancamento.id_lancamento))
