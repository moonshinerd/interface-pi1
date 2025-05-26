
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


def criar_figura_gps_mapa(telemetrias) -> go.Figure:
    telemetrias = list(telemetrias)
    if not telemetrias:
        return go.Figure()

    lats = [t.latitude for t in telemetrias]
    lons = [t.longitude for t in telemetrias]

    fig = go.Figure(go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode='lines+markers',    # desenha rota e pontos
        marker=dict(size=6),
        line=dict(width=2)
    ))

    fig.update_layout(
        mapbox_style='open-street-map',
        mapbox=dict(
            center=dict(lat=sum(lats)/len(lats), lon=sum(lons)/len(lons)),
            zoom=18.499999999999998, 
        ),
        uirevision='gps-map',
        margin=dict(l=0, r=0, t=30, b=0),
        title='Trajetória GPS'
    )
    return fig