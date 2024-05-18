import os
from django.shortcuts import render

from foto_crud.upload_image import ImgurUpload

from ..models import Photo, User, Topic, PhotoTopic, Album, AlbumPhoto
import json
from django.http import JsonResponse

# Create your views here.
def upload_photo(request):
    if request.method == 'GET': 
        user = request.COOKIES['cookie']
        user = User.objects.filter(cookies=user).first().username
        return render(request, 'upload-image.html', {'user': user})
    else:
        photo = request.FILES['img']
        photo_saved_link = 'E:\DUT Courses\Academic year r3\Semester 2\Lập trình Python\Photo-sharing\Foto\photos/' + photo.name
        with open(photo_saved_link, 'wb+') as destination:
            for chunk in photo.chunks():
                destination.write(chunk)

        photo = photo_saved_link

        imgur = ImgurUpload()
        try:
            photo_link = imgur.upload_image_from_image_path(photo)
        except:
            return JsonResponse({'message': 'Upload ảnh thất bại'})
        print(photo_link)
        # delete photo after upload
        os.remove(photo_saved_link)

        author = request.COOKIES['cookie']
        author = User.objects.filter(cookies=author).first()

        photo = Photo(photo_link=photo_link, author=author)
        photo.save()

        topics_uploaded = request.POST['theme'].split(',')
        print(topics_uploaded)
        topics = []
        for t in topics_uploaded:
            if Topic.objects.filter(topic_name=t).first() is None:
                topic = Topic(topic_name=t)
                topic.save()
                topics.append(topic)
            else:
                topics.append(Topic.objects.filter(topic_name=t).first())

        for t in topics:
            photo_topic = PhotoTopic(photo_id=photo.photo_id, topic_id=t.topic_id)
            photo_topic.save()

        album_name = 'Tất cả ảnh đã upload của ' + author.username
        # create album if not exist
        album = Album.objects.filter(album_name=album_name, author=author).first()
        if album is None:
            album = Album(album_name=album_name, author=author)
            album.save()
        album_photo = AlbumPhoto(album=album, photo=photo, user=author)
        album_photo.save()

        return JsonResponse({'status': 'success'})
        
    
def save_photo(request):
    photo_id = request.GET['photo_id']
    user = request.COOKIES['cookie']
    user = User.objects.get(cookies=user).first()
    saved_photo = AlbumPhoto.objects.get(photo=photo_id, user=user).first()
    if saved_photo is not None:
        return render(request, 'foto_crud/index.html', {'message': 'Ảnh đã được lưu'})
    user = request.COOKIES['cookie']
    user = User.objects.get(cookies=user).first()
    photo = Photo.objects.get(photo_id=photo_id).first()
    album = request.GET['album']
    album = Album.objects.get(album_name=album, author=user).first()
    saved_photo = AlbumPhoto(user=user, photo=photo, album=album)
    saved_photo.save()
    return render(request, 'foto_crud/index.html')

def create_album(request):
    if request.method == 'GET':
        return render(request, 'foto_crud/create_album.html')
    else:
        album_name = request.POST['album_name']
        author = request.COOKIES['cookie']
        author = User.objects.get(cookies=author).first()
        album = Album.objects.get(album_name=album_name, author=author).first()
        if album is None:
            album = Album(album_name=album_name, author=author)
            album.save()
            return render(request, 'foto_crud/create_album.html', {'message': 'Tạo album thành công'})
        else:
            return render(request, 'foto_crud/create_album.html', {'message': 'Album đã tồn tại'})

def upvote_photo(request):
    photo_id = request.GET['photo_id']
    photo = Photo.objects.get(photo_id=photo_id).first()
    photo.upvotes += 1
    photo.save()
    return render(request, 'foto_crud/index.html')

def remove_photo(request):
    if request.method == 'GET':
        return render(request, 'foto_crud/remove_photo.html')
    else:
        # remove one photo
        photo_id = request.POST['photo_id']
        album = request.POST['album']
        author = request.COOKIES['cookie']
        author = User.objects.get(cookies=author).first()
        record = AlbumPhoto.objects.get(user=author, photo=photo_id, album=album).first()
        record.delete()
        return render(request, 'foto_crud/remove_photo.html', {'message': 'Xóa ảnh thành công'})
    
def remove_multiple_photo(request):
    if request.method == 'GET':
        return render(request, 'foto_crud/remove_photo.html')
    else:
        # remove multiple photos
        photo_ids = request.POST['photo_ids']
        album = request.POST['album']
        author = request.COOKIES['cookie']
        author = User.objects.get(cookies=author).first()
        for photo_id in photo_ids:
            record = AlbumPhoto.objects.get(user=author, photo=photo_id, album=album).first()
            record.delete()

        albums = Album.objects.filter(author=author).all()
        return render(request, 'foto_crud/remove_photo.html', {'message': 'Xóa ảnh thành công'})
    
def remove_album(request):
    if request.method == 'GET':
        return render(request, 'foto_crud/remove_album.html')
    else:
        album_name = request.POST['album_name']
        author = request.COOKIES['cookie']
        author = User.objects.get(cookies=author).first()
        album = Album.objects.get(album_name=album_name, author=author).first()
        album.delete()

        for album_photo in AlbumPhoto.objects.filter(album=album).all():
            album_photo.delete()

        return render(request, 'foto_crud/remove_album.html', {'message': 'Xóa album thành công'})
    



