from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ajax/municipios/', views.carregar_municipios, name='ajax_municipios'),
    path('', views.conscrito, name='conscrito'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('buscar/', views.buscar, name='buscar'),
    path('entrevista/<str:pk>/', views.entrevista, name='entrevista'),
    path('material/<str:pk>/', views.material, name='material'),
    path('medica/<str:pk>/', views.medico, name='medica'),
    path('odonto/<str:pk>/', views.odonto, name='odonto'),
    path('social/<str:pk>/', views.social, name='social'),
]