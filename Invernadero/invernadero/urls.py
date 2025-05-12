from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('api/', include('api_comunication.urls')),
    path('disable-2fa/', views.disable_2fa, name='disable_2fa'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('reenviar-activacion/', views.reenviar_activacion, name='reenviar_activacion'),
]