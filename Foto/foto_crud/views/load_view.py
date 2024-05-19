from django.shortcuts import render
from ..models import Photo, User, Topic, PhotoTopic, Album, AlbumPhoto
from .helpers import (
    get_user_from_cookie,
    get_photos_by_user,
    get_author_and_album,
    get_photos_by_album_and_author,
    get_albums_by_author,
    get_other_photos
)


def home(request):
    try:
        user_cookie = request.COOKIES['cookie']
        user = get_user_from_cookie(user_cookie)
    except:
        user = None
        
    albums = get_albums_by_author(user)
    other_photos = get_other_photos(user)
    return render(request, 'home.html', {'user': user, 
                                         'albums': albums, 
                                         'other_photos': other_photos})

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
    if request.GET.get('album') is not None:
        return load_image_by_album(request)
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


def photoOfAlbum(request):
    return render(request, 'photos-of-album.html')

# This function holds the logic for loading the search profile page, but it is not implemented yet.


def load_user_search(request):
    return render(request, 'search-profile.html',
                  {
                      'searchText': request.GET.get('search'),
                      'users': User.objects.filter(username__icontains=request.GET.get('search')).all(),
                      'count': User.objects.filter(username__icontains=request.GET.get('search')).count()
                  })


def load_guest_profile(request):
    current_user = get_user_from_cookie(request.COOKIES['cookie'])
    albums = Album.objects.filter(author=current_user).all()
    user = request.GET.get('username')
    # query userId
    user = User.objects.filter(username=user).first()
    if user:
        photos = Photo.objects.filter(author_id=user).all()
    else:
        return render(request, 'guest-visit.html', {'error': 'User not found'})
    return render(request, 'guest-visit.html', {
        'user': user,
        'photos': photos,
        'photoCount': 15,
        'albums': albums
    })

def load_gallery(request):
    TOPICS1 = ['natural', 'fashion', 'animals']
    TOPICS2 = ['lifestyle', 'city', 'country']
    current_user = get_user_from_cookie(request.COOKIES['cookie'])
    photos = get_other_photos(current_user)[0:5]
    gallery = []
    index = 0
    for photo in photos:
        gallery.append({
            "photo": photo,
            "topics": str(TOPICS1[index % 3] + ' ' + TOPICS2[index % 3])
        })
        index += 1
    albums = Album.objects.filter(author=current_user).all()
    return render(request, 'gallery.html', {'gallery': gallery, 'albums': albums})

def load_image_by_album(request):
    username = request.COOKIES['cookie']
    user = get_user_from_cookie(username)
    album_name = request.GET.get('album')
    album = Album.objects.filter(album_name=album_name, author=user.username).first()
    photosInAlbum = AlbumPhoto.objects.filter(album=album).all()
    photos = []
    for photoInAlbum in photosInAlbum:
        # query photo
        photo = Photo.objects.filter(photo_id=photoInAlbum.photo_id).first()
        photos.append(photo)
    return render(request, 'photos-of-album.html', {'photos': photos, "album_name": album_name, "photos_count": len(photos)})