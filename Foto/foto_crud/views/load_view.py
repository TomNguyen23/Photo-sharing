from django.shortcuts import render
from ..models import Photo, User, Topic, PhotoTopic, Album, AlbumPhoto

def home(request):
    user = request.user
    return render(request, 'home.html', {'user': user})

def load_own_photo(request):
    user_cookie = request.COOKIES['cookie']
    user = User.objects.filter(cookies=user_cookie).first().username
    photos = AlbumPhoto.objects.filter(user_id=user).all()
    result = [Photo.objects.filter(photo_id=photo.photo_id).first().photo_link for photo in photos]
    return render(request, 'profile-manager.html', {'user': user, 'photos': result})

def load_other_photo(request):
    author = request.GET['author']
    author = User.objects.filter(username=author).first()
    album = request.GET['album']
    album = Album.objects.filter(album_name=album, author=author).first()
    photos = AlbumPhoto.objects.filter(album=album, user=author).all()
    result = [Photo.objects.filter(photo_id=photo.photo).first().photo_link for photo in photos]
    return render(request, 'foto_crud/load_other_photo.html', {'photos': result})

def load_album(request):
    user_cookie = request.COOKIES['cookie']
    user = User.objects.filter(cookies=user_cookie).first()
    albums = Album.objects.filter(author=user).all()
    result = [album.album_name for album in albums]
    return render(request, 'my-albums.html', {'user': user, 'albums': result})

def load_other_album(request):
    author = request.GET['author']
    author = User.objects.filter(username=author).first()
    albums = Album.objects.filter(author=author).all()
    result = [album.album_name for album in albums]
    return render(request, 'foto_crud/load_other_album.html', {'albums': result})
