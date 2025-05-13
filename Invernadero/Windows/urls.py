from django.urls import path
from .views import landing, home


urlpatterns = [
    path('', landing, name="landing"),
    path('home/', home, name="home")
]