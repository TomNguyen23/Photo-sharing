import os
from ..models import Photo, Topic, User, Album, AlbumPhoto

def get_user_from_cookie(cookie):
    return User.objects.filter(cookies=cookie).first()

def get_photos_by_user(user):
    photos = AlbumPhoto.objects.filter(user=user).all()
    return [Photo.objects.filter(photo_id=photo.photo_id).first() for photo in photos]

def get_author_and_album(author_username, album_name):
    author = User.objects.filter(username=author_username).first()
    album = Album.objects.filter(album_name=album_name, author=author).first()
    return author, album

def get_photos_by_album_and_author(album, author):
    photos = AlbumPhoto.objects.filter(album=album, user=author).all()
    return [Photo.objects.filter(photo_id=photo.photo).first() for photo in photos]

def get_albums_by_author(author):
    albums = Album.objects.filter(author=author).all()
    return [album.album_name for album in albums]

# function to get all photos of other users except mine
def get_other_photos(user):
    photos = AlbumPhoto.objects.exclude(user=user).all()
    return Photo.objects.filter(photo_id__in=[photo.photo_id for photo in photos]).all()

def handle_photo_upload(photo_file):
    try:
        local_photo_path = '../Foto/Foto_crud/photos/' + photo_file.name
        with open(local_photo_path, 'wb+') as destination:
            for chunk in photo_file.chunks():
                destination.write(chunk)
        return local_photo_path
    except Exception as e:
        raise Exception(f"Error in handle_photo_upload: {e}")

def get_author_from_request(request):
    try:
        author_cookie = request.COOKIES['cookie']
        author = User.objects.filter(cookies=author_cookie).first()
        return author
    except Exception as e:
        raise Exception(f"Error in get_author_from_request: {e}")

def get_or_create_topic(topic_name):
    try:
        topic = Topic.objects.filter(topic_name=topic_name).first()
        if topic is None:
            topic = Topic(topic_name=topic_name)
            topic.save()
        return topic
    except Exception as e:
        raise Exception(f"Error in get_or_create_topic: {e}")

def get_or_create_album(album_name, author):
    try:
        album = Album.objects.filter(album_name=album_name, author=author).first()
        if album is None:
            album = Album(album_name=album_name, author=author)
            album.save()
        return album
    except Exception as e:
        raise Exception(f"Error in get_or_create_album: {e}")

def handle_album_photo_save(album, photo, author):
    try:
        album_photo = AlbumPhoto(album=album, photo=photo, user=author)
        album_photo.save()
    except Exception as e:
        raise Exception(f"Error in handle_album_photo_save: {e}")

def handle_photo_removal(photo_id, album_name, author):
    try:
        photo = Photo.objects.filter(photo_id=photo_id).first()
        album = Album.objects.filter(album_name=album_name).first()
        photo_to_remove = AlbumPhoto.objects.filter(user=author, photo=photo, album=album).first()
        if photo_to_remove:
            photo_to_remove.delete()
    except Exception as e:
        raise Exception(f"Error in handle_photo_removal: {e}")
