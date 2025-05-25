from django.shortcuts import render, get_object_or_404
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
  
def detalhe_lancamento(request, pk):
    lancamento = get_object_or_404(Lancamento, pk=pk)
    telemetrias = lancamento.telemetrias.all()
    return render(request, 'oldlaunches/detail.html', {
        'lancamento': lancamento,
        'telemetrias': telemetrias
    })
