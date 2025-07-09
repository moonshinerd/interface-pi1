from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
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


@csrf_exempt
def iniciar_lancamento(request):
    """Inicia um novo lançamento"""
    if request.method == 'POST':
        # Verifica se já existe um lançamento ativo
        lancamento_ativo = Lancamento.objects.filter(data_hora_fim__isnull=True).first()
        if lancamento_ativo:
            return JsonResponse({
                'success': False,
                'message': 'Já existe um lançamento ativo. Finalize-o primeiro.'
            })
        
        # Obtém a distância do request
        import json
        try:
            data = json.loads(request.body)
            distancia_alvo = float(data.get('distancia_alvo', 10.0))
        except (json.JSONDecodeError, ValueError, TypeError):
            distancia_alvo = 10.0
        
        # Valida se a distância é uma das opções permitidas
        distancias_validas = [10.0, 20.0, 30.0]
        if distancia_alvo not in distancias_validas:
            distancia_alvo = 10.0
        
        # Cria novo lançamento
        lancamento = Lancamento.objects.create(
            data_hora_inicio=timezone.now(),
            data_hora_fim=None,
            volume_agua=750.0,
            angulo=45.0,
            pressao_lancamento=53.03,
            distancia_alvo=distancia_alvo
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Lançamento {lancamento.id_lancamento} iniciado com sucesso! Distância alvo: {distancia_alvo} m',
            'lancamento_id': lancamento.id_lancamento,
            'distancia_alvo': distancia_alvo
        })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})


@csrf_exempt
def finalizar_lancamento(request):
    """Finaliza o lançamento ativo"""
    if request.method == 'POST':
        lancamento_ativo = Lancamento.objects.filter(data_hora_fim__isnull=True).first()
        
        if not lancamento_ativo:
            return JsonResponse({
                'success': False,
                'message': 'Não há lançamento ativo para finalizar.'
            })
        
        lancamento_ativo.data_hora_fim = timezone.now()
        lancamento_ativo.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Lançamento {lancamento_ativo.id_lancamento} finalizado com sucesso!',
            'lancamento_id': lancamento_ativo.id_lancamento
        })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})


def status_lancamento(request):
    """Retorna o status atual do lançamento"""
    lancamento_ativo = Lancamento.objects.filter(data_hora_fim__isnull=True).first()
    
    if lancamento_ativo:
        telemetrias_count = lancamento_ativo.telemetrias.count()
        return JsonResponse({
            'ativo': True,
            'lancamento_id': lancamento_ativo.id_lancamento,
            'inicio': lancamento_ativo.data_hora_inicio.isoformat(),
            'telemetrias_count': telemetrias_count
        })
    else:
        return JsonResponse({
            'ativo': False,
            'message': 'Nenhum lançamento ativo'
        })
