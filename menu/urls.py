from django.urls import path
from .views import home, menu_carta, agregar, lista_carrito, eliminar, guardar_pedido, ordenar_confirmacion, generar_pdf

urlpatterns = [
    path('home/',home, name='home'),
    path('carta/',menu_carta, name='carta'),
    path('agregar/<int:item_id>/', agregar, name='agregar'),
    path('carrito/', lista_carrito, name='carrito'),
    path('eliminar/<int:item_id>/', eliminar, name='eliminar'),
    path('guardar_pedido/', guardar_pedido, name='guardar_pedido'),
    path('ordenar_confirmacion/<int:order_id>/', ordenar_confirmacion, name='ordenar_confirmacion'),
    path('menu/generar_pdf/<int:ordenar_id>/', generar_pdf, name='generar_pdf'),

]
