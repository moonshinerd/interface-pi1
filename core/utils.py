
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
