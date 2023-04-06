from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from eshop.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('authentication.urls')),
    path('accounts/', include('allauth.urls')),
    
    path('', Home.as_view(), name='home'),
    path('shop/', include('eshop.urls')),
    path('order/', include('order.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
