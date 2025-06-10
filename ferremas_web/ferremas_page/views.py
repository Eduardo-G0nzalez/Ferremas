from .models import Producto
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .forms import RegistroFormPersonalizado
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from datetime import date, timedelta
import uuid
import requests
import xml.etree.ElementTree as ET
from .transbank_config import transaction
from decimal import Decimal
from django.http import JsonResponse
import json
from .models import MensajeContacto
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from .models import MensajeContacto
from django.contrib.auth.decorators import login_required
from .models import Compra, CompraItem

# Create your views here.
def home(request):
    return render(request, 'index.html')

def home_view(request):
    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos': productos})

def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'producto.html', {'producto': producto})

def productos_view(request):
    productos = Producto.objects.all()
    
    categorias = sorted(set(producto.categoria for producto in productos if producto.categoria))

    categoria_filtrada = request.GET.get('categoria')
    if categoria_filtrada:
        productos = productos.filter(categoria=categoria_filtrada)

    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_activa': categoria_filtrada
    }
    return render(request, 'productos.html', context)

def acceso_unificado(request):
    login_form = AuthenticationForm()
    registro_form = RegistroFormPersonalizado()

    if request.method == 'POST':
        if 'password1' in request.POST:
            registro_form = RegistroFormPersonalizado(request.POST)
            if registro_form.is_valid():
                user = registro_form.save()
                auth_login(request, user)
                return redirect('/')
        else:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                auth_login(request, login_form.get_user())
                return redirect('/')

    return render(request, 'login.html', {
        'login_form': login_form,
        'registro_form': registro_form
    })

@login_required
def iniciar_pago(request):
    carrito = request.session.get('carrito', {})
    
    if not carrito:
        return render(request, 'error_pago.html', {'error': 'El carrito está vacío.'})

    total = 0
    for producto_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id=producto_id)
            total += producto.precio * cantidad
        except Producto.DoesNotExist:
            continue

    total = int(total)

    buy_order = str(uuid.uuid4())[:12]
    session_id = str(uuid.uuid4())[:12]
    return_url = request.build_absolute_uri(reverse('webpay_confirmacion'))

    try:
        response = transaction.create(buy_order, session_id, total, return_url)
        return redirect(response['url'] + '?token_ws=' + response['token'])
    except Exception as e:
        return render(request, 'error_pago.html', {'error': str(e)})



def webpay_confirmacion(request):
    token = request.GET.get('token_ws')

    if not token:
        return render(request, 'error_pago.html', {'error': 'Token no recibido'})

    try:
        result = transaction.commit(token)

        if result['status'] == 'AUTHORIZED':
            carrito = request.session.get('carrito', {})
            productos = Producto.objects.filter(id__in=carrito.keys())

            total = 0
            for producto in productos:
                cantidad = carrito.get(str(producto.id), 0)
                total += producto.precio * cantidad

            # Crear la compra
            compra = Compra.objects.create(
                usuario=request.user,
                email=request.user.email,
                total=total,
                orden=result['buy_order'],
                estado='pagado'
                )

            for producto in productos:
                cantidad = carrito.get(str(producto.id), 0)

                if producto.stock >= cantidad:
                    producto.stock -= cantidad
                    producto.save()

                    CompraItem.objects.create(
                        compra=compra,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=producto.precio
                    )
                else:
                    print(f"No hay suficiente stock para {producto.nombre}")

            # Vaciar el carrito
            request.session['carrito'] = {}

            return render(request, 'pago_exitoso.html', {
                'monto': result['amount'],
                'orden': result['buy_order'],
                'fecha': result['transaction_date']
            })
        else:
            return render(request, 'error_pago.html', {'error': 'Transacción rechazada'})

    except Exception as e:
        return render(request, 'error_pago.html', {'error': str(e)})
    


def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())

    carrito_detalle = []
    total = Decimal(0)

    for producto in productos:
        cantidad = carrito[str(producto.id)]
        subtotal = producto.precio * cantidad
        total += subtotal
        carrito_detalle.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    # --- Conversión de moneda ---
    moneda = request.GET.get('moneda', 'CLP')
    tipo_cambio = None
    precio_convertido = None

    if moneda != 'CLP':
        tipo_cambio = obtener_tipo_cambio(moneda)
        if tipo_cambio:
            precio_convertido = round(float(total) / tipo_cambio, 2)

    context = {
        'carrito': carrito_detalle,
        'total': total,
        'precio_convertido': precio_convertido,
        'tipo_cambio': tipo_cambio,
        'moneda_actual': moneda,
    }

    return render(request, 'carrito.html', context)


def agregar_al_carrito(request, producto_id):
    producto = Producto.objects.get(id=producto_id)

    if producto.stock <= 0:
        messages.error(request, "Este producto no tiene stock disponible.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        if carrito[str(producto_id)] >= producto.stock:
            messages.error(request, "Has alcanzado el stock disponible de este producto.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        carrito[str(producto_id)] += 1
    else:
        carrito[str(producto_id)] = 1

    request.session['carrito'] = carrito
    messages.success(request, "Producto agregado al carrito exitosamente.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def agregar_desde_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto = get_object_or_404(Producto, id=producto_id)
    producto_id_str = str(producto_id)

    # Obtener cuántos ya hay en el carrito
    cantidad_en_carrito = carrito.get(producto_id_str, 0)

    # Verificar si hay stock suficiente
    if cantidad_en_carrito < producto.stock:
        carrito[producto_id_str] = cantidad_en_carrito + 1
        request.session['carrito'] = carrito
    else:
        messages.warning(request, f"No hay más stock disponible para el producto: {producto.nombre}")

    return redirect('ver_carrito')


def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id_str = str(producto_id)

    if producto_id_str in carrito:
        if carrito[producto_id_str] > 1:
            carrito[producto_id_str] -= 1
        else:
            del carrito[producto_id_str]
        request.session['carrito'] = carrito

    return redirect('ver_carrito')


def obtener_tipo_cambio(moneda='USD'):
    url = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx'
    user = 'edugonzalezsilva72@gmail.com'
    password = 'L@lito007informatica'

    series = {
        'USD': 'F073.TCO.PRE.Z.D',
        'EUR': 'F072.CLP.EUR.N.O.D'
    }

    fecha = date.today()

    for _ in range(5):
        date_str = fecha.strftime('%Y-%m-%d')
        params = {
            'user': user,
            'pass': password,
            'function': 'GetSeries',
            'timeseries': series.get(moneda),
            'firstdate': date_str,
            'lastdate': date_str,
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if data.get("Codigo") == 0:
                observaciones = data.get("Series", {}).get("Obs", [])
                if observaciones:
                    return float(observaciones[0].get("value"))
                else:
                    print(f"⚠️ No hay datos de tipo de cambio para {moneda} en {date_str}")
            else:
                print(f" Error del Banco Central: {data.get('Descripcion')}")

        except Exception as e:
            print(f" Error al procesar JSON para {moneda} en {date_str}: {e}")

        fecha -= timedelta(days=1)

    print(f" No se pudo obtener tipo de cambio para {moneda}")
    return None


def vista_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    tipo_cambio = obtener_tipo_cambio('USD') 

    precio_usd = None
    if tipo_cambio:
        precio_usd = round(producto.precio / tipo_cambio, 2)

    return render(request, 'producto_detalle.html', {
        'producto': producto,
        'precio_usd': precio_usd,
        'tipo_cambio': tipo_cambio,
        'moneda_actual': 'USD'
    })

@csrf_exempt
def enviar_mensaje_json(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mensaje = MensajeContacto.objects.create(
                nombre=data.get('nombre'),
                email=data.get('email'),
                asunto=data.get('asunto'),
                mensaje=data.get('mensaje')
            )
            return JsonResponse({'estado': 'ok', 'mensaje': '¡Hemos recibido tu mensaje, nos contactaremos muy pronto contigo!'})
        except Exception as e:
            return JsonResponse({'estado': 'error', 'detalle': str(e)}, status=400)
    return JsonResponse({'estado': 'error', 'mensaje': 'Método no permitido'}, status=405)

def tipo_cambio_api(request):
    moneda = request.GET.get('moneda', 'USD')
    tipo_cambio = obtener_tipo_cambio(moneda)
    if tipo_cambio:
        return JsonResponse({'moneda': moneda, 'tipo_cambio': tipo_cambio})
    else:
        return JsonResponse({'error': 'No se pudo obtener el tipo de cambio'}, status=400)

