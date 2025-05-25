from django.shortcuts import render
from plotly.io import to_html
from .models import Lancamento
from .utils import criar_figura_aceleracao

def graficos_teste(request):
    lanc = Lancamento.objects.prefetch_related('telemetrias').first()
    if not lanc:
        graph_html = "<p>Nenhum dado disponível</p>"
    else:
        times = [t.data_hora for t in lanc.telemetrias.all()]
        accel_x = [t.aceleracao_x for t in lanc.telemetrias.all()]
        fig = criar_figura_aceleracao(times, accel_x)
        graph_html = to_html(fig, include_plotlyjs=False, full_html=False)

    return render(request, "core/graficos_testes.html", {"graph_html": graph_html})

def lista_lancamentos(request):
    lancamentos = Lancamento.objects.all().order_by('-data_hora_inicio').prefetch_related('telemetrias')
    return render(request, "core/launch_list.html", {"lancamentos": lancamentos})
