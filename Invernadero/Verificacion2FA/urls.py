from django.urls import path
from Verificacion2FA import views

urlpatterns = [
    path('disable-2fa/', views.disable_2fa, name='disable_2fa')
]