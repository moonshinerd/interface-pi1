# core/management/commands/seed_realistic.py

import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Lancamento, Telemetria

class Command(BaseCommand):
    help = 'Popula o banco com 3 lançamentos (10m, 20m, 30m) – 25 leituras cada, 45° e 750 mL'

    def handle(self, *args, **options):
        # Cada tupla: (alcance_m, tempo_total_s)
        scenarios = [
            (10, 1.4),   # para ~10 m
            (20, 2.0),   # para ~20 m
            (30, 2.5),   # para ~30 m
        ]

        for alcance, duracao in scenarios:
            inicio = timezone.now()
            fim    = inicio + timedelta(seconds=duracao)
            lanc = Lancamento.objects.create(
                data_hora_inicio=inicio,
                data_hora_fim=fim,
            )
            self.stdout.write(f"Criado Lançamento {lanc.id_lancamento}: ≈{alcance} m em ≈{duracao}s")

            # Divide o período em 24 intervalos (25 pontos)
            interval = duracao / 24.0
            for i in range(25):
                t  = i * interval
                ts = inicio + timedelta(seconds=t)

                # Aceleração Z: de 9.81 → 0; X/Y em função da fase
                az = 9.81 * max(0, 1 - t/duracao)
                factor = 1 - abs(2 * t/duracao - 1)
                ax = random.uniform(-1, 1) * factor
                ay = random.uniform(-1, 1) * factor

                # Giroscópio: mais instável no início/fim
                peak = lambda: random.uniform(-50, 50)
                mid  = lambda: random.uniform(-5, 5)
                gx = peak() if t < 0.3 or t > duracao - 0.3 else mid()
                gy = peak() if t < 0.3 or t > duracao - 0.3 else mid()
                gz = peak() if t < 0.3 or t > duracao - 0.3 else mid()

                # Altitude e vela. solo: sobe e depois desce
                if t <= duracao/2:
                    alt = alcance * (t / (duracao/2))
                    spd = (alcance / (duracao/2)) * t
                else:
                    alt = alcance * ((duracao - t) / (duracao/2))
                    spd = (alcance / (duracao/2)) * (duracao - t)

                # Bateria simulada
                bus_v  = 4.2 - 0.2 * (t / duracao)
                cur_mA = 100 + 200 * (t / duracao)
                shunt  = cur_mA * 0.001
                pwr    = bus_v * cur_mA

                Telemetria.objects.create(
                    lancamento    = lanc,
                    data_hora     = ts,
                    aceleracao_x  = round(ax, 2),
                    aceleracao_y  = round(ay, 2),
                    aceleracao_z  = round(az, 2),
                    vel_angular_x = round(gx, 1),
                    vel_angular_y = round(gy, 1),
                    vel_angular_z = round(gz, 1),
                    latitude      = round(-15.7929 + random.uniform(-0.00005, 0.00005), 6),
                    longitude     = round(-47.8828 + random.uniform(-0.00005, 0.00005), 6),
                    altitude      = round(max(0, alt), 2),
                    vel_sob_solo  = round(abs(spd), 2),
                    shunt_voltage = round(shunt, 3),
                    bus_voltage   = round(bus_v, 2),
                    current_mA    = round(cur_mA, 1),
                    power_mW      = round(pwr, 1),
                )

            self.stdout.write(self.style.SUCCESS(
                f"Lançamento {lanc.id_lancamento}: {lanc.telemetrias.count()} leituras criadas."
            ))
