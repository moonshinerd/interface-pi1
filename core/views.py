from django.shortcuts import render, get_object_or_404
from plotly.io import to_html
from .models import Lancamento
from .utils import criar_figura_aceleracao, criar_figura_gps_3d

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
    fig_3d        = criar_figura_gps_3d(telemetrias)
    gps_3d_html   = fig_3d.to_html(full_html=False, include_plotlyjs='cdn')
    return render(request, 'oldlaunches/detail.html', {
        'lancamento': lancamento,
        'telemetrias': telemetrias,
        'gps_3d_plot_html': gps_3d_html,
    })

def lista_lancamentos(request):
    lancamentos = Lancamento.objects.all().order_by('-data_hora_inicio').prefetch_related('telemetrias')
    return render(request, "core/launch_list.html", {"lancamentos": lancamentos})

