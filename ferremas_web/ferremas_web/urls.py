"""
URL configuration for ferremas_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from ferremas_page.views import home_view, enviar_mensaje_json
from ferremas_page import views
from django.contrib.auth.views import LogoutView
from ferremas_page.views import tipo_cambio_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('productos/', views.productos_view, name='productos'),
    path('productos/categoria/<slug:slug>/', views.productos_view, name='productos_por_categoria'),
    path('acceso/', views.acceso_unificado, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/', include('allauth.urls')),
    path('pago/', views.iniciar_pago, name='iniciar_pago'),
    path('webpay/confirmacion/', views.webpay_confirmacion, name='webpay_confirmacion'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/agregar-desde-carrito/<int:producto_id>/', views.agregar_desde_carrito, name='agregar_desde_carrito'),
    path('api/contacto/', enviar_mensaje_json, name='api_contacto'),
    path('api/tipo-cambio/', tipo_cambio_api, name='tipo_cambio_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
