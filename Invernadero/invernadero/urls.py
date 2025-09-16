from django.contrib import admin
from django.urls import path, include
from users import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('api/', include('api_comunication.urls')),
    path('Verificion2FA/', include('Verificacion2FA.urls')),
    path('ResetPassword/', include('Authentication.urls')),
    path('', include('Windows.urls')),
    path('diagnostico/', include('diagnostico.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)