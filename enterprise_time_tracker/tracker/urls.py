from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('action/', views.action, name='action'),
    path('export/', views.export_csv, name='export_csv'),
]
