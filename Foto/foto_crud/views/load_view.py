from django.shortcuts import render

from models import Photo, SavedPhoto, User, Topic, PhotoTopic, Album, AlbumPhoto

def load_own_photo(request):
    user = request.COOKIES['cookie']
    user = User.objects.get(cookies=user).first()
    album = request.GET['album']
    album = Album.objects.get(album_name=album, author=user).first()
    photos = AlbumPhoto.objects.filter(album=album).all()
    result = []
    for photo in photos:
        link = Photo.objects.get(photo_id=photo.photo).first().photo_link
        result.append(link)
    return render(request, 'foto_crud/load_own_photo.html', {'photos': result})

def load_other_photo(request):
    author = request.GET['author']
    author = User.objects.get(username=author).first()
    album = request.GET['album']
    album = Album.objects.get(album_name=album, author=author).first()
    photos = AlbumPhoto.objects.filter(album=album, user=author).all()
    result = []
    for photo in photos:
        link = Photo.objects.get(photo_id=photo.photo).first().photo_link
        result.append(link)
    return render(request, 'foto_crud/load_other_photo.html', {'photos': result})

def load_album(request):
    user = request.COOKIES['cookie']
    user = User.objects.get(cookies=user).first()
    albums = Album.objects.filter(author=user).all()
    result = []
    for album in albums:
        result.append(album.album_name)
    return render(request, 'foto_crud/load_album.html', {'albums': result})

def load_other_album(request):
    author = request.GET['author']
    author = User.objects.get(username=author).first()
    albums = Album.objects.filter(author=author).all()
    result = []
    for album in albums:
        result.append(album.album_name)
    return render(request, 'foto_crud/load_other_album.html', {'albums': result})
