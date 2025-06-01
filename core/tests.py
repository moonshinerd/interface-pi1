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

class TelemetriaModelTest(TestCase):
    def setUp(self):
        self.lancamento = Lancamento.objects.create(
            data_hora_inicio=timezone.now(),
            data_hora_fim=timezone.now()
        )

    def test_criar_telemetria_completa(self):
        telemetria = Telemetria.objects.create(
            lancamento=self.lancamento,
            data_hora=timezone.now(),
            aceleracao_x=1.0,
            aceleracao_y=2.0,
            aceleracao_z=3.0,
            vel_angular_x=4.0,
            vel_angular_y=5.0,
            vel_angular_z=6.0,
            latitude=-23.5505,
            longitude=-46.6333,
            altitude=100.0
        )
        self.assertIsNotNone(telemetria.pk)
        self.assertEqual(telemetria.aceleracao_x, 1.0)
        self.assertEqual(telemetria.latitude, -23.5505)

    def test_telemetria_campos_opcionais(self):
        telemetria = Telemetria.objects.create(
            lancamento=self.lancamento,
            data_hora=timezone.now(),
            aceleracao_x=1.0,
            aceleracao_y=2.0,
            aceleracao_z=3.0,
            vel_angular_x=4.0,
            vel_angular_y=5.0,
            vel_angular_z=6.0
        )
        self.assertIsNone(telemetria.latitude)
        self.assertIsNone(telemetria.longitude)

class UtilsTest(TestCase):
    def setUp(self):
        self.lancamento = Lancamento.objects.create(
            data_hora_inicio=timezone.now(),
            data_hora_fim=timezone.now()
        )
        self.telemetrias = [
            Telemetria.objects.create(
                lancamento=self.lancamento,
                data_hora=timezone.now(),
                aceleracao_x=1.0,
                aceleracao_y=2.0,
                aceleracao_z=3.0,
                vel_angular_x=4.0,
                vel_angular_y=5.0,
                vel_angular_z=6.0,
                latitude=-23.5505,
                longitude=-46.6333,
                altitude=100.0
            )
        ]

    def test_criar_figura_aceleracao_x_tempo(self):
        fig = criar_figura_aceleracao_x_tempo(self.telemetrias)
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(len(fig.data), 3)

    def test_criar_figura_gps_3d(self):
        fig = criar_figura_gps_3d(self.telemetrias)
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(len(fig.data), 1) 

    def test_criar_figura_tensao_potencia(self):
        fig = criar_figura_tensao_potencia(self.telemetrias)
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(len(fig.data), 4)

class ViewsTest(TestCase):
    def setUp(self):
        self.lancamento = Lancamento.objects.create(
            data_hora_inicio=timezone.now(),
            data_hora_fim=timezone.now()
        )

    def test_home_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    def test_lancamento_detail_view(self):
        response = self.client.get(f'/oldlaunches/{self.lancamento.id_lancamento}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oldlaunches/detail.html')

    def test_telemetria_view(self):
        response = self.client.get(f'/oldlaunches/{self.lancamento.id_lancamento}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oldlaunches/detail.html')

class UrlsTest(TestCase):
    def test_urls_resolvem_para_views_corretas(self):
        from django.urls import resolve
        from core import views
        from django.views.generic import TemplateView

        url = resolve('/')
        self.assertTrue(isinstance(url.func, type(TemplateView.as_view())))

        url = resolve(f'/oldlaunches/1/')
        self.assertEqual(url.func, views.detalhe_lancamento)

        url = resolve('/oldlaunches/')
        self.assertEqual(url.func, views.lista_lancamentos)
