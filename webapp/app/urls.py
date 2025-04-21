from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from home.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls'), name='users'),
    path('cuoora/', include('cuoora.urls'), name='cuoora')
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
