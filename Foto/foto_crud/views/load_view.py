from django.shortcuts import render
from ..models import Photo, User, Topic, PhotoTopic, Album, AlbumPhoto
from .helpers import (
    get_user_from_cookie, 
    get_photos_by_user, 
    get_author_and_album, 
    get_photos_by_album_and_author,
    get_albums_by_author
)

def home(request):
    user = request.user
    return render(request, 'home.html', {'user': user})

def load_own_photo(request):
    user_cookie = request.COOKIES['cookie']
    user = get_user_from_cookie(user_cookie)
    if user:
        photos = get_photos_by_user(user)
        return render(request, 'profile-manager.html', {'user': user.username, 'photos': photos})
    else:
        return render(request, 'profile-manager.html', {'error': 'User not found'})

def load_other_photo(request):
    author_username = request.GET.get('author')
    album_name = request.GET.get('album')
    author, album = get_author_and_album(author_username, album_name)
    if author and album:
        photos = get_photos_by_album_and_author(album, author)
        return render(request, 'foto_crud/load_other_photo.html', {'photos': photos})
    else:
        return render(request, 'foto_crud/load_other_photo.html', {'error': 'Author or album not found'})

def load_album(request):
    user_cookie = request.COOKIES['cookie']
    user = get_user_from_cookie(user_cookie)
    if user:
        albums = get_albums_by_author(user)
        return render(request, 'my-albums.html', {'user': user.username, 'albums': albums})
    else:
        return render(request, 'my-albums.html', {'error': 'User not found'})

def load_other_album(request):
    author_username = request.GET.get('author')
    author = User.objects.filter(username=author_username).first()
    if author:
        albums = get_albums_by_author(author)
        return render(request, 'foto_crud/load_other_album.html', {'albums': albums})
    else:
        return render(request, 'foto_crud/load_other_album.html', {'error': 'Author not found'})
