from django.urls import path
from . import mainViews

urlpatterns = [
    path('', mainViews.home, name='home'),
    path('gallery/', mainViews.gallery, name='gallery'),
    path('sign-in/', mainViews.sign_in, name='sign-in'),
    path('sign-up/', mainViews.sign_up, name='sign-up'),
    path('profile/', mainViews.profile, name='profile'),
    path('my-albums/', mainViews.my_albums, name='my-albums'),
]