from django.shortcuts import render

from models import Photo, User, Topic, PhotoTopic, Album, AlbumPhoto

# Create your views here.
def upload_photo(request):
    if request.method == 'GET': 
        return render(request, 'foto_crud/upload_photo.html')
    else:
        photo = request.FILES['photo']
        photo_link = 'photos/' + photo.name
        with open(photo_link, 'wb+') as destination:
            for chunk in photo.chunks():
                destination.write(chunk)
        author = request.COOKIES['cookie']
        author = User.objects.get(cookies=author).first()

        photo = Photo(photo_link=photo_link, author=author)
        photo.save()

        topic = request.POST['topic']
        topic = Topic.objects.get(topic_name=topic).all()

        for t in topic:
            photo_topic = PhotoTopic(photo=photo, topic=t)
            photo_topic.save()

        album = request.POST['album']
        if album:
            album = Album.objects.get(album_name=album, author=author).first()
            album_photo = AlbumPhoto(album=album, photo=photo)
            album_photo.save()
        else:
            album_name = 'Tất cả ảnh của ' + author.username
            # create album if not exist
            album = Album.objects.get(album_name=album_name, author=author).first()
            if album is None:
                album = Album(album_name=album_name, author=author)
                album.save()
            album_photo = AlbumPhoto(album=album, photo=photo)
            album_photo.save()

        return render(request, 'foto_crud/upload_photo.html', {'message': 'Upload ảnh thành công'})
    
def remove_photo(request):
    if request.method == 'GET':
        author = request.COOKIES['cookie']
        author = User.objects.get(cookies=author).first()
        photos = Photo.objects.filter(author=author)
        return render(request, 'foto_crud/remove_photo.html', {'photos': photos})
    else:
        photo_id = request.POST['photo_id']
        photo = Photo.objects.get(photo_id=photo_id)
        photo.delete()
        return render(request, 'foto_crud/remove_photo.html', {'message': 'Xóa ảnh thành công'})