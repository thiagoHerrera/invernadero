from django.urls import path
from .views import signin, signup, landing

urlpatterns = [
    
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('', landing, name="landing"),
]
