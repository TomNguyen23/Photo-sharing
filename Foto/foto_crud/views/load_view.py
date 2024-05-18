from django.shortcuts import render

# from ..models import Photo, SavedPhoto, User, Topic, PhotoTopic, Album, AlbumPhoto
from ..models import Photo, User, Topic, PhotoTopic, Album, AlbumPhoto

def home(request):
    user = request.user
    return render(request, 'home.html', {'user': user})

def load_own_photo(request):
    user = request.COOKIES['cookie']
    user = User.objects.filter(cookies=user).first().username
    photos = AlbumPhoto.objects.filter(user_id=user).all()
    result = []
    for photo in photos:
        link = Photo.objects.filter(photo_id=photo.photo_id).first().photo_link
        result.append(link)
    return render(request, 'profile-manager.html', {'user': user,
                                                    'photos': result})

def load_other_photo(request):
    author = request.filter['author']
    author = User.objects.filter(username=author).first()
    album = request.get['album']
    album = Album.objects.filter(album_name=album, author=author).first()
    photos = AlbumPhoto.objects.filter(album=album, user=author).all()
    result = []
    for photo in photos:
        link = Photo.objects.filter(photo_id=photo.photo).first().photo_link
        result.append(link)
    return render(request, 'foto_crud/load_other_photo.html', {'photos': result})

def load_album(request):
    user = request.COOKIES['cookie']
    user = User.objects.filter(cookies=user).first()
    albums = Album.objects.filter(author=user).all()
    result = []
    for album in albums:
        result.append(album.album_name)
    return render(request, 'my-albums.html', {'user': user, 'albums': result})

def load_other_album(request):
    author = request.get['author']
    author = User.objects.filter(username=author).first()
    albums = Album.objects.filter(author=author).all()
    result = []
    for album in albums:
        result.append(album.album_name)
    return render(request, 'foto_crud/load_other_album.html', {'albums': result})

