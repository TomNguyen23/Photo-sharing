from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context = {
        'title': 'Foto',
        'content': 'Welcome to Foto',
    }
    return render(request, 'home.html', context=context)

def gallery(request):
    context = {
    }
    return render(request, 'gallery.html', context=context)

def sign_in(request):
    context = {
    }
    return render(request, 'sign-in.html', context=context)

def sign_up(request):
    context = {
    }
    return render(request, 'sign-up.html', context=context)

def profile(request):
    context = {
    }
    return render(request, 'profile-manager.html', context=context)

def my_albums(request):
    context = {
    }
    return render(request, 'my-albums.html', context=context)