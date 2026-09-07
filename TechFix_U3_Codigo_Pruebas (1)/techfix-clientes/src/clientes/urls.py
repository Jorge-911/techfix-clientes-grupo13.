from django.urls import path
from . import views
app_name = "clientes"
urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("clientes/nuevo/", views.nuevo, name="nuevo"),
    path("clientes/<int:pk>/", views.detalle, name="detalle"),
    path("clientes/<int:pk>/editar/", views.editar, name="editar"),
]
