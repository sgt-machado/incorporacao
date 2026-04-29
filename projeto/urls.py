from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('atualizar/', views.buscar_conscrito, name='buscar_cpf'),
    path('atualizar/<int:pk>/', views.editar_dados, name='editar_dados'),
    path('ajax/municipios/', views.carregar_municipios, name='ajax_municipios'),
]