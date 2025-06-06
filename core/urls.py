# urls.py (correto)
from django.urls import path
from django.views.generic import TemplateView
from core import views



urlpatterns = [
    path('newlaunch/', TemplateView.as_view(template_name="core/launch_new.html")),
    path('oldlaunches/', views.lista_lancamentos, name="oldlaunches"),
    path('', TemplateView.as_view(template_name="core/home.html")),
    path('oldlaunches/<int:pk>/', views.detalhe_lancamento, name='oldlaunch-detail'),
]   