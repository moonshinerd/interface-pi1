# urls.py (correto)
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('newlaunch/', TemplateView.as_view(template_name="core/launch_new.html")),
    path('oldlaunches/', TemplateView.as_view(template_name="core/launch_list.html")),
    path('', TemplateView.as_view(template_name="core/base.html")),
]   