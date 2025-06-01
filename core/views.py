from django.shortcuts import render, get_object_or_404
from plotly.io import to_html
from .models import Lancamento
from .utils import criar_figura_aceleracao_x_tempo, criar_figura_velocidade_angular, criar_figura_gps_3d, criar_figura_gps_mapa#, criar_figura_tensao_potencia



def detalhe_lancamento(request, pk):
    lancamento = get_object_or_404(Lancamento, pk=pk)
    telemetrias = lancamento.telemetrias.order_by('data_hora')

    gps_fig      = criar_figura_gps_mapa(telemetrias)
    gps_map_html = gps_fig.to_html(full_html=False, include_plotlyjs='cdn')
      
    # fig_vp = criar_figura_tensao_potencia(telemetrias)
    # vp_plot_html = to_html(fig_vp, include_plotlyjs='cdn', full_html=False)

    angvel_fig = criar_figura_velocidade_angular(telemetrias)
    angvel_html = angvel_fig.to_html(full_html=False, include_plotlyjs='cdn')

    acel_fig = criar_figura_aceleracao_x_tempo(telemetrias)
    acel_html = acel_fig.to_html(full_html=False, include_plotlyjs='cdn')

    fig_3d        = criar_figura_gps_3d(telemetrias)
    gps_3d_html   = fig_3d.to_html(full_html=False, include_plotlyjs='cdn')

    return render(request, 'oldlaunches/detail.html', {
        'lancamento': lancamento,
        'telemetrias': telemetrias,
        
        'gps_map_plot_html': gps_map_html,
        # 'vp_plot_html': vp_plot_html,
        'angvel_plot_html': angvel_html,
        'acceleration_plot_html': acel_html,
        'gps_3d_plot_html': gps_3d_html,
    })
    

def lista_lancamentos(request):
    lancamentos = Lancamento.objects.all().order_by('-data_hora_inicio').prefetch_related('telemetrias')
    return render(request, "core/launch_list.html", {"lancamentos": lancamentos})
