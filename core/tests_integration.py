from django.test import TestCase
from django.urls import reverse
from core.models import Lancamento, Telemetria
from django.utils import timezone
from core.utils import (
    criar_figura_aceleracao_x_tempo,
    criar_figura_gps_3d,
    criar_figura_tensao_potencia,
    criar_figura_gps_mapa,
    criar_figura_velocidade_angular
)

class LancamentoTelemetriaIntegrationTest(TestCase):
    def setUp(self):
        self.lancamento = Lancamento.objects.create(
            data_hora_inicio=timezone.now(),
            data_hora_fim=timezone.now(),
            volume_agua=750.0,
            angulo=45.0,
            pressao_lancamento=53.03,
            distancia_alvo=10.0
        )
        
        self.telemetrias = []
        for i in range(5):
            telemetria = Telemetria.objects.create(
                lancamento=self.lancamento,
                data_hora=timezone.now(),
                aceleracao_x=float(i),
                aceleracao_y=float(i + 1),
                aceleracao_z=float(i + 2),
                vel_angular_x=float(i),
                vel_angular_y=float(i + 1),
                vel_angular_z=float(i + 2),
                latitude=-23.5505 + (i * 0.0001),
                longitude=-46.6333 + (i * 0.0001),
                altitude=100.0 + i,
                shunt_voltage=3.3 + i,
                bus_voltage=5.0 + i,
                current_mA=100.0 + i,
                power_mW=500.0 + i
            )
            self.telemetrias.append(telemetria)

    def test_fluxo_completo_lancamento_telemetria(self):
        """Testa o fluxo completo de um lançamento com suas telemetrias"""
        self.assertEqual(Lancamento.objects.count(), 1)
        self.assertEqual(self.lancamento.telemetrias.count(), 5)

        telemetrias_ordenadas = self.lancamento.telemetrias.all()
        self.assertEqual(len(telemetrias_ordenadas), 5)

        fig_acel = criar_figura_aceleracao_x_tempo(telemetrias_ordenadas)
        self.assertEqual(len(fig_acel.data), 3)  # X, Y, Z

        fig_gps = criar_figura_gps_3d(telemetrias_ordenadas)
        self.assertEqual(len(fig_gps.data), 1)

        fig_tensao = criar_figura_tensao_potencia(telemetrias_ordenadas)
        self.assertEqual(len(fig_tensao.data), 4)

        fig_mapa = criar_figura_gps_mapa(telemetrias_ordenadas)
        self.assertEqual(len(fig_mapa.data), 1)

        fig_vel = criar_figura_velocidade_angular(telemetrias_ordenadas)
        self.assertEqual(len(fig_vel.data), 3)
