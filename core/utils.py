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