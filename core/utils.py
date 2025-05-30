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
