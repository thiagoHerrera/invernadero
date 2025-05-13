from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def landing(request):
    return render(request, 'landing.html')
# Create your views here.
