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
    user = request.user
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
    
def load_photo_topic(request):
    user_cookie = request.COOKIES['cookie']
    user = get_user_from_cookie(user_cookie)

    photos_excluded = get_other_photos(user)

    for photo in photos_excluded:
        print (photo.photo_link)

    result = []

    for photo in photos_excluded:
        result_object = {}
        result_object['photo'] = photo.photo_link

        topics = PhotoTopic.objects.filter(photo=photo).all()
        topic_names = [topic.topic.topic_name for topic in topics]

        topic_result = []
        for topic_name in topic_names:
            topic_result.append(topic_name)

        result_object['topics'] = topic_result
        result.append(result_object)

    print (result)

    return render(request, 'example.html', {'photos': result})
