from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Menu, Ordenar, OrdenarItem
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Create your views here.

def home(request):
    return render(request, 'menu/home.html')

def menu_carta(request):
    menu = Menu.objects.all()
    return render(request, 'menu/carta_menu.html', {'menu': menu})

def agregar(request, item_id):
    item = get_object_or_404(Menu, id=item_id)
    cantidad = int(request.POST.get('cantidad', 1))

    
    if 'carrito' not in request.session or not isinstance(request.session['carrito'], dict):
        request.session['carrito'] = {}

    carrito = request.session['carrito']

    if str(item_id) in carrito:
        carrito[str(item_id)] += cantidad
    else:
        carrito[str(item_id)] = cantidad

    request.session.modified = True  
    return redirect('carta')

def lista_carrito(request):
    carrito = request.session.get("carrito", {})
    carrito_items = []
    for item_id, cantidad in carrito.items():
        item = get_object_or_404(Menu, id=item_id)
        item.cantidad = cantidad
        carrito_items.append(item)
    return render(request, 'menu/pedido_menu.html', {'carrito_items': carrito_items})

def guardar_pedido(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('carrito')  

    ordenar = Ordenar.objects.create()
    for item_id, cantidad in carrito.items():
        menu_item = get_object_or_404(Menu, id=item_id)
        OrdenarItem.objects.create(ordenar=ordenar, menu_item=menu_item, cantidad=cantidad)

    request.session['carrito'] = {}  # Limpiar el carrito después de guardar el pedido
    return redirect('ordenar_confirmacion', order_id=ordenar.id)

def eliminar(request, item_id):
    carrito = request.session.get('carrito', {})
    if str(item_id) in carrito:
        del carrito[str(item_id)]
    request.session['carrito'] = carrito
    return redirect('carrito')

def ordenar_confirmacion(request, order_id):
    ordenar = get_object_or_404(Ordenar, id=order_id)
    total = sum(item.menu_item.precio * item.cantidad for item in ordenar.items.all())
    return render(request, 'menu/ordenar_confirmacion.html', {'ordenar': ordenar, 'total': total})

def generar_pdf(request, ordenar_id):
    ordenar = get_object_or_404(Ordenar, id=ordenar_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="pedido_{ordenar_id}.pdf"'

    # Crear el PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Título del documento
    p.drawString(100, height - 50, "Factura")
    p.drawString(100, height - 70, f"Pedido ID: {ordenar_id}")

    # Encabezados de la tabla
    p.drawString(100, height - 100, "Nombre")
    p.drawString(300, height - 100, "Precio")
    p.drawString(400, height - 100, "Cantidad")

    y = height - 120
    total = 0

    for item in ordenar.ordenaritem_set.all():
        p.drawString(100, y, item.menu_item.nombre)
        p.drawString(300, y, f"${item.menu_item.precio}")
        p.drawString(400, y, str(item.cantidad))
        total += item.menu_item.precio * item.cantidad
        y -= 20

    p.drawString(100, y - 20, f"Total a pagar: ${total}")

    p.showPage()
    p.save()

    return response
