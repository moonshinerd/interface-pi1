# core/management/commands/seed_launches.py

import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Lancamento, Telemetria

class Command(BaseCommand):
    help = (
        'Popula 6 lançamentos: 2×10m, 2×20m, 2×30m (45°, 750mL), '
        'com 30 leituras de telemetria cada'
    )

    def handle(self, *args, **options):
        g = 9.81  # gravidade m/s²
        # Cenários: (distância_alvo, tempo_de_voo, pressão_integral)
        # Calculamos v0 = sqrt(R*g), T = 2*v0*sin45/g = sqrt(2R/g)
        scenarios = {
            10.0: {
                'T': (2 * (10.0 * g)**0.5 * 0.7071) / g,                 # ≈1.43 s
                'psi': 53.03 * ((10.0 * g)**0.5)**2 / ((20.0 * g)**0.5)**2  # ≈26.5 PSI (base 20m→53.03)
            },
            20.0: {
                'T': (2 * (20.0 * g)**0.5 * 0.7071) / g,                 # ≈2.02 s
                'psi': 53.03                                             # referência
            },
            30.0: {
                'T': (2 * (30.0 * g)**0.5 * 0.7071) / g,                 # ≈2.47 s
                'psi': 53.03 * ((30.0 * g)**0.5)**2 / ((20.0 * g)**0.5)**2  # ≈79.5 PSI
            },
        }

        for distancia, params in scenarios.items():
            for rep in range(2):  # gera 2 lançamentos por distância
                inicio = timezone.now() + timedelta(minutes=random.randint(0, 30))
                duracao = params['T']
                fim = inicio + timedelta(seconds=duracao)
                psi = round(params['psi'], 2)

                lanc = Lancamento.objects.create(
                    data_hora_inicio=inicio,
                    data_hora_fim=fim,
                    volume_agua=750.0,
                    angulo=45.0,
                    pressao_lancamento=psi,
                    distancia_alvo=distancia
                )
                self.stdout.write(f"🔹 Lançamento {lanc.id_lancamento}: {distancia} m → T={duracao:.2f}s, P={psi} PSI")

                # 30 leituras uniformes no intervalo [0, duracao]
                for i in range(30):
                    t = duracao * i / 29
                    ts = inicio + timedelta(seconds=t)
                    # aceleração Z decai de 9.81→0, X/Y variação menor no meio
                    az = 9.81 * max(0, 1 - t/duracao)
                    factor = 1 - abs(2*t/duracao - 1)
                    ax = random.uniform(-1, 1) * factor
                    ay = random.uniform(-1, 1) * factor
                    # giroscópio: picos no início/fim
                    peak = lambda: random.uniform(-50, 50)
                    mid  = lambda: random.uniform(-5, 5)
                    gx = peak() if t < 0.3 or t > duracao-0.3 else mid()
                    gy = peak() if t < 0.3 or t > duracao-0.3 else mid()
                    gz = peak() if t < 0.3 or t > duracao-0.3 else mid()
                    # altitude sobe até metade e depois desce
                    if t <= duracao/2:
                        alt = distancia * (t/(duracao/2))
                        spd = (distancia/(duracao/2)) * t
                    else:
                        alt = distancia * ((duracao-t)/(duracao/2))
                        spd = (distancia/(duracao/2)) * (duracao-t)

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
                    )

                self.stdout.write(self.style.SUCCESS(
                    f"    → {lanc.telemetrias.count()} leituras geradas."
                ))
