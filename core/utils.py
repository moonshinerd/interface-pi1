import plotly.graph_objects as go

def criar_figura_aceleracao_x_tempo(telemetrias) -> go.Figure:
    # Garante que telemetrias esteja ordenado por data_hora
    telemetrias = list(telemetrias)  
    if not telemetrias:
        return go.Figure()

    t0 = telemetrias[0].data_hora
    times_ms = []
    accel_x = []
    accel_y = []
    accel_z = []

    for t in telemetrias:
        dt = t.data_hora
        # Delta total em microssegundos e conversão para ms inteiro
        delta_us = (dt - t0).total_seconds() * 1_000_000  
        rel_ms = int(delta_us // 1000)  
        times_ms.append(rel_ms)

        accel_x.append(t.aceleracao_x)
        accel_y.append(t.aceleracao_y)
        accel_z.append(t.aceleracao_z)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times_ms, y=accel_x, mode='lines', name='X'))
    fig.add_trace(go.Scatter(x=times_ms, y=accel_y, mode='lines', name='Y'))
    fig.add_trace(go.Scatter(x=times_ms, y=accel_z, mode='lines', name='Z'))

    fig.update_layout(
        title='Aceleração vs Tempo (ms desde início)',
        xaxis_title='Tempo (ms)',
        yaxis_title='Aceleração (m/s²)',
        legend=dict(
            orientation='h',
            yanchor='bottom', y=1.02,
            xanchor='right', x=1
        ),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def criar_figura_gps_3d(telemetrias) -> go.Figure:
    telemetrias = list(telemetrias)
    if not telemetrias:
        return go.Figure()

    # Extrai listas de coordenadas
    lons = [t.longitude for t in telemetrias]
    lats = [t.latitude  for t in telemetrias]
    alts = [t.altitude  for t in telemetrias]

    fig = go.Figure(go.Scatter3d(
        x=lons,
        y=lats,
        z=alts,
        mode='lines+markers',
        line=dict(width=2,
                  color = 'blue'),
        marker = dict(
                  size = 2,
                  color = 'red',)
    ))
  
    fig.update_layout(
        title='Trajetória GPS 3D',
        scene=dict(
            xaxis_title='Longitude (m)',
            yaxis_title='Latitude (m)',
            zaxis_title='Altitude (m)'
        ),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    return fig


def criar_figura_tensao_potencia(telemetrias) -> go.Figure:
    telemetrias = list(telemetrias)
    if not telemetrias:
        return go.Figure()
    t0 = telemetrias[0].data_hora

    times_ms = []
    shunt    = []
    bus      = []
    current  = []
    power    = []

    for t in telemetrias:
        delta_us = (t.data_hora - t0).total_seconds() * 1_000_000
        rel_ms   = int(delta_us // 1000)
        times_ms.append(rel_ms)

        shunt.append(t.shunt_voltage or 0)
        bus.append(t.bus_voltage   or 0)
        current.append(t.current_mA or 0)
        power.append(t.power_mW     or 0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times_ms, y=shunt,   mode='lines', name='Shunt V'))
    fig.add_trace(go.Scatter(x=times_ms, y=bus,     mode='lines', name='Bus V'))
    fig.add_trace(go.Scatter(x=times_ms, y=current, mode='lines', name='Corrente (mA)'))
    fig.add_trace(go.Scatter(x=times_ms, y=power,   mode='lines', name='Potência (mW)'))

    fig.update_layout(
        title=f'Tensão & Potência vs Tempo (ms desde início) Lançamento #{telemetrias[0].lancamento.id_lancamento}',
        xaxis_title='Tempo (ms)',
        yaxis_title='Valor',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    return fig

def criar_figura_velocidade_angular(telemetrias) -> go.Figure:
    telemetrias = list(telemetrias)
    if not telemetrias:
        return go.Figure()
    
    t0 = telemetrias[0].data_hora

    times_str = []
    angvel_x = []
    angvel_y = []
    angvel_z = []

    for t in telemetrias:
        dt = t.data_hora
        millis = dt.microsecond // 1000
        ms_str = f"{millis:03d}"
        timestamp = dt.strftime(f"%H:%M:%S.{ms_str}")
        times_str.append(timestamp)

        angvel_x.append(t.vel_angular_x)
        angvel_y.append(t.vel_angular_y)
        angvel_z.append(t.vel_angular_z)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times_str, y=angvel_x, mode='lines', name='X',  line=dict(color='#d90429')))
    fig.add_trace(go.Scatter(x=times_str, y=angvel_y, mode='lines', name='Y', line=dict(color='#8d99ae')))
    fig.add_trace(go.Scatter(x=times_str, y=angvel_z, mode='lines', name='Z', line=dict(color='#2b2d42')))

    fig.update_layout(
        title='Velocidade Angular vs Tempo (hh:mm:ss.mmm)',
        xaxis_title='Tempo',
        yaxis_title='Velocidade Angular',
        legend=dict(
            orientation='h',
            yanchor='bottom', y=1.02,
            xanchor='right',  x=1
        ),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

