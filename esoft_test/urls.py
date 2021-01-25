from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('enderecos.urls')), #configura a raiz do servidor como o app 'Enderecos'
]
