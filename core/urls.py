# urls.py (correto)
from django.urls import path
from django.views.generic import TemplateView
from . import views



urlpatterns = [
    path('newlaunch/', TemplateView.as_view(template_name="core/launch_new.html")),
    path('oldlaunches/', views.lista_lancamentos, name="oldlaunches"),
    path('home/', TemplateView.as_view(template_name="core/home.html")),
    path('', TemplateView.as_view(template_name="core/base.html")),
    path('graficosteste/', views.graficos_teste, name='graficosteste'),
]   