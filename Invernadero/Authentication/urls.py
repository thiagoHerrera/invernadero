from django.contrib.auth import views as auth_views
from django.urls import path
from Verificacion2FA import views

urlpatterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        success_url='/ResetPassword/password_reset_done/'
    ), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/ResetPassword/password_reset_complete/'
    ), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('reenviar-activacion/', views.reenviar_activacion, name='reenviar_activacion'),
]