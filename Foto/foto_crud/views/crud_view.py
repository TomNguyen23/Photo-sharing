import os
from django.shortcuts import render
from django.http import JsonResponse

from foto_crud.upload_image import ImgurUpload
from ..models import Photo, User, Topic, PhotoTopic, Album, AlbumPhoto
from .helpers import (
    get_user_from_cookie, 
    get_photos_by_user, 
    get_author_and_album, 
    get_photos_by_album_and_author,
    get_albums_by_author
)
import json

# Create your views here.
def upload_photo(request):
    if request.method == 'GET': 
        user_cookie = request.COOKIES['cookie']
        user = get_user_from_cookie(user_cookie)
        albums = get_albums_by_author(user)
        return render(request, 'upload-image.html', {'albums': albums})
    else:
        photo_file = request.FILES['img']
        local_photo_path =  'E:\DUT Courses\Academic year r3\Semester 2\Lập trình Python\Photo-sharing\Foto\photos/' + photo_file.name

        with open(local_photo_path, 'wb+') as destination:
            for chunk in photo_file.chunks():
                destination.write(chunk)

        imgur = ImgurUpload()
        try:
            imgur_photo_link = imgur.upload_image_from_image_path(local_photo_path)
        except:
            return JsonResponse({'message': 'Upload ảnh thất bại'})
        
        os.remove(local_photo_path)

        author_cookie = request.COOKIES['cookie']
        author = User.objects.filter(cookies=author_cookie).first()

        new_photo = Photo(photo_link=imgur_photo_link, author=author)
        new_photo.save()

        topics_uploaded = request.POST['theme'].split(',')
        topics = []

        for topic_name in topics_uploaded:
            topic = Topic.objects.filter(topic_name=topic_name).first()
            if topic is None:
                topic = Topic(topic_name=topic_name)
                topic.save()
            topics.append(topic)

        for topic in topics:
            photo_topic = PhotoTopic(photo=new_photo, topic=topic)
            photo_topic.save()

        album_name = request.POST['album']
        if album_name:
            album = Album.objects.filter(album_name=album_name, author=author).first()
        else:
            album_name = f'Tất cả ảnh đã upload của {author.username}'
            album = Album.objects.filter(album_name=album_name, author=author).first()
            if album is None:
                album = Album(album_name=album_name, author=author)
                album.save()

        album_photo = AlbumPhoto(album=album, photo=new_photo, user=author)
        album_photo.save()

        return JsonResponse({'status': 'success'})

def save_photo(request):
    photo_id = request.GET['photo_id']
    user_cookie = request.COOKIES['cookie']
    user = User.objects.filter(cookies=user_cookie).first()

    if AlbumPhoto.objects.filter(photo_id=photo_id, user=user).exists():
        return render(request, 'foto_crud/index.html', {'message': 'Ảnh đã được lưu'})

    photo = Photo.objects.filter(photo_id=photo_id).first()
    album_name = request.GET['album']
    album = Album.objects.filter(album_name=album_name, author=user).first()

    saved_photo = AlbumPhoto(user=user, photo=photo, album=album)
    saved_photo.save()

    return render(request, 'foto_crud/index.html')

def create_album(request):
    album_name = request.POST['new-album']
    author_cookie = request.COOKIES['cookie']
    author = User.objects.filter(cookies=author_cookie).first()

    if not Album.objects.filter(album_name=album_name, author=author).exists():
        album = Album(album_name=album_name, author=author)
        album.save()

    albums = Album.objects.filter(author=author)
    album_names = [album.album_name for album in albums]

    return JsonResponse({'status': 'success', 'albums': album_names})

def upvote_photo(request):
    photo_id = request.GET['photo_id']
    photo = Photo.objects.filter(photo_id=photo_id).first()
    photo.upvotes += 1
    photo.save()
    return render(request, 'foto_crud/index.html')

def remove_photo(request):
    if request.method == 'GET':
        return render(request, 'foto_crud/remove_photo.html')
    else:
        photo_id = request.POST['photo_id']
        album_name = request.POST['album']
        author_cookie = request.COOKIES['cookie']
        author = User.objects.filter(cookies=author_cookie).first()

        photo_to_remove = AlbumPhoto.objects.filter(user=author, photo_id=photo_id, album__album_name=album_name).first()
        photo_to_remove.delete()

        return render(request, 'foto_crud/remove_photo.html', {'message': 'Xóa ảnh thành công'})

def remove_multiple_photos(request):
    if request.method == 'GET':
        return render(request, 'foto_crud/remove_photo.html')
    else:
        photo_ids = request.POST.getlist('photo_ids')
        album_name = request.POST['album']
        author_cookie = request.COOKIES['cookie']
        author = User.objects.filter(cookies=author_cookie).first()

        for photo_id in photo_ids:
            photo_to_remove = AlbumPhoto.objects.filter(user=author, photo_id=photo_id, album__album_name=album_name).first()
            photo_to_remove.delete()

        return render(request, 'foto_crud/remove_photo.html', {'message': 'Xóa ảnh thành công'})

def remove_album(request):
    album_name = request.GET['album']
    author_cookie = request.COOKIES['cookie']
    author = User.objects.filter(cookies=author_cookie).first()

    album_to_remove = Album.objects.filter(album_name=album_name, author_id=author).first()
    
    AlbumPhoto.objects.filter(album=album_to_remove).delete()
    album_to_remove.delete()

    return JsonResponse({'status': 'success'})
