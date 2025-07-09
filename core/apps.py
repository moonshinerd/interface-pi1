# core/apps.py
import threading
import time
import sys
from datetime import datetime, timedelta

import requests
from django.apps import AppConfig
from django.conf import settings

def fetch_remote_telemetria(timeout=5, interval=1):
    url = getattr(settings, 'ESP32_API_URL', 'http://127.0.0.1:8080/api/telemetria')
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = requests.get(url, timeout=2)
            resp.raise_for_status()
            data = resp.json()
            # Validação mínima
            for k in ('accelX','gyroX','year'):
                if k not in data:
                    raise ValueError('JSON incompleto')
            return data
        except requests.exceptions.RequestException as e:
            print(f"Erro de rede ao buscar telemetria: {e}")
            time.sleep(interval)
        except ValueError as e:
            print(f"Erro de validação JSON: {e}")
            time.sleep(interval)
        except Exception as e:
            print(f"Erro inesperado ao buscar telemetria: {e}")
            time.sleep(interval)
    return None

def telemetry_worker():
    # Importa os models só quando o thread iniciar
    from .models import Telemetria, Lancamento

    interval = getattr(settings, 'TELEMETRY_POLL_INTERVAL', 2)
    
    print("Worker de telemetria iniciado - aguardando lançamento ativo...")
    
    while True:
        try:
            # Busca apenas lançamentos ativos (sem data_hora_fim)
            lanc = Lancamento.objects.filter(data_hora_fim__isnull=True).order_by('-id_lancamento').first()
            
            if lanc:
                print(f"Monitorando lançamento ativo: {lanc}")
                
                data = fetch_remote_telemetria()
                if data:
                    dt = datetime(
                        year=int(data['year']),
                        month=int(data['month']),
                        day=int(data['day']),
                        hour=int(data['hour']),
                        minute=int(data['minute']),
                        second=int(data['second']),
                    )
                    telemetria = Telemetria.objects.create(
                        lancamento      = lanc,
                        data_hora       = dt,
                        aceleracao_x    = data['accelX'],
                        aceleracao_y    = data['accelY'],
                        aceleracao_z    = data['accelZ'],
                        vel_angular_x   = data['gyroX'],
                        vel_angular_y   = data['gyroY'],
                        vel_angular_z   = data['gyroZ'],
                        temperatura     = data['tempC'],
                        latitude        = data['latitude'],
                        longitude       = data['longitude'],
                        altitude        = data['altitude'],
                        velocidade      = data['speed'],
                    )
                    print(f"Telemetria registrada: {telemetria} - {dt}")
                else:
                    print("Falha ao buscar telemetria do ESP32")
            else:
                print("Nenhum lançamento ativo - aguardando...")
                time.sleep(interval)
                continue
                
        except Exception as e:
            print(f"Erro no worker de telemetria: {e}")
        
        time.sleep(interval)

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # Não importa models aqui!
        # Só dispara o worker depois que tudo estiver pronto
        if 'runserver' in sys.argv or 'uwsgi' in sys.argv:
            t = threading.Thread(target=telemetry_worker, daemon=True)
            t.start()
