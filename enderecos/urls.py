from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='endereco-home'), #redireciona o cliente para a view 'home'
    path('create/', views.create, name='endereco-create'), #redireciona o cliente para a view 'create'
]
