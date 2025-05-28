
import plotly.graph_objects as go

def criar_figura_aceleracao(times, accel_x):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times,
        y=accel_x,
        mode='lines+markers',
        name='Aceleração X',
        line=dict(color='#3a5f6f') # define a cor da linha
    ))
    fig.update_layout(
        xaxis_title='Data/Hora',
        yaxis_title='Aceleração (m/s²)'
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
