from django.contrib import admin
from django.urls import path, include
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('api/', include('api_comunication.urls')),
    path('Verificion2FA/', include('Verificacion2FA.urls')),
    path('ResetPassword/', include('Authentication.urls')),
    path('', include('Windows.urls'))
]