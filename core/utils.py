import plotly.graph_objects as go

def criar_figura_aceleracao(times, accel_x):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times,
        y=accel_x,
        mode='lines+markers',
        name='Aceleração X',
        line=dict(color='#3a5f6f')  
    ))
    fig.update_layout(
        xaxis_title='Data/Hora',
        yaxis_title='Aceleração (m/s²)'
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
