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
from ferremas_page.views import home_view
from ferremas_page import views
from django.contrib.auth.views import LogoutView

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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
