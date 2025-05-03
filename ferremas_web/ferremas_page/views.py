from .models import Producto
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .forms import RegistroFormPersonalizado
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .transbank_config import transaction
from django.urls import reverse
from .transbank_config import transaction
import uuid

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

def iniciar_pago(request):
    buy_order = str(uuid.uuid4())[:12]  # Orden única de compra (máx 26 caracteres)
    session_id = str(uuid.uuid4())[:12]  # ID de sesión único
    amount = 1000  # Monto en pesos chilenos
    return_url = request.build_absolute_uri(reverse('webpay_confirmacion'))

    try:
        response = transaction.create(buy_order, session_id, amount, return_url)
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
            return render(request, 'pago_exitoso.html', {
                'monto': result['amount'],
                'orden': result['buy_order'],
                'fecha': result['transaction_date']
            })
        else:
            return render(request, 'error_pago.html', {'error': 'Transacción rechazada'})

    except Exception as e:
        return render(request, 'error_pago.html', {'error': str(e)})


