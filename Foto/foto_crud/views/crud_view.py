import os
from django.shortcuts import render
from django.http import JsonResponse

from foto_crud.upload_image import ImgurUpload
from foto_crud.views.helpers import handle_photo_upload
from ..models import Photo, User, Topic, PhotoTopic, Album, AlbumPhoto
import json
import logging
from .helpers import (handle_photo_upload, get_author_from_request, 
                     get_or_create_topic, get_or_create_album, 
                     handle_album_photo_save, handle_photo_removal)

# Create your views here.


def upload_photo(request):
    if request.method == 'GET': 
        user_cookie = request.COOKIES['cookie']
        user = get_user_from_cookie(user_cookie)
        albums = get_albums_by_author(user)
        return render(request, 'upload-image.html', {'albums': albums})
    else:
        try:  # Add try block here
            photo_file = request.FILES['img']
            local_photo_path = handle_photo_upload(photo_file)

            imgur = ImgurUpload()
            try:
                imgur_photo_link = imgur.upload_image_from_image_path(local_photo_path)
            except Exception as e:
                logging.error(f"Imgur upload failed: {e}")
                return JsonResponse({'message': 'Upload ảnh thất bại'})
            finally:
                os.remove(local_photo_path)

            author = get_author_from_request(request)
            new_photo = Photo(photo_link=imgur_photo_link, author=author)
            new_photo.save()

            topics_uploaded = request.POST['theme'].split(',')
            topics = [get_or_create_topic(topic_name) for topic_name in topics_uploaded]

            for topic in topics:
                PhotoTopic(photo=new_photo, topic=topic).save()

            album_name = request.POST.get('album', f'Tất cả ảnh đã upload của {author.username}')
            if (album_name == ''):
                album_name = f'Tất cả ảnh đã upload của {author.username}'
            album = get_or_create_album(album_name, author)
            handle_album_photo_save(album, new_photo, author)
            if not album_name == f'Tất cả ảnh đã upload của {author.username}':
                album_name = f'Tất cả ảnh đã upload của {author.username}'
                album = get_or_create_album(album_name, author)
                handle_album_photo_save(album, new_photo, author)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            logging.error(f"Error in upload_photo: {e}")
            return JsonResponse({'message': 'Không thể upload ảnh, hãy thử lại'})

def save_photo(request):
    try:
        photo_id = request.POST['photo_id']
        user = get_author_from_request(request)

        if AlbumPhoto.objects.filter(photo_id=photo_id, user=user).exists():
            return render(request, 'foto_crud/index.html', {'message': 'Ảnh đã được lưu'})

        photo = Photo.objects.filter(photo_id=photo_id).first()
        album_name = request.POST['album']
        album = Album.objects.filter(album_name=album_name, author=user).first()

        AlbumPhoto(user=user, photo=photo, album=album).save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        logging.error(f"Error in save_photo: {e}")
        return JsonResponse({'message': 'Không thể lưu ảnh, hãy thử lại'})

def create_album(request):
    try:
        album_name = request.POST['new-album']
        author = get_author_from_request(request)

        if Album.objects.filter(album_name=album_name, author=author).exists():
            return JsonResponse({'status': 'fail', 'message': 'Album đã tồn tại'})

        Album(album_name=album_name, author=author).save()

        albums = Album.objects.filter(author=author)
        album_names = [album.album_name for album in albums]

        return JsonResponse({'status': 'success', 'albums': album_names})
    except Exception as e:
        logging.error(f"Error in create_album: {e}")
        return JsonResponse({'message': 'Không thể tạo mới album, hãy thử lại'})

def upvote_photo(request):
    try:
        photo_id = request.GET['photo_id']
        photo = Photo.objects.filter(photo_id=photo_id).first()
        photo.upvotes += 1
        photo.save()
        return render(request, 'foto_crud/index.html')
    except Exception as e:
        logging.error(f"Error in upvote_photo: {e}")
        return JsonResponse({'message': 'Không thể upvote ảnh, hãy thử lại'})
def remove_photo(request):
    try:
        if request.method == 'GET':
            return render(request, 'foto_crud/remove_photo.html')

        photo_id = request.POST['photo_id']
        album_name = request.POST['album']
        author = get_author_from_request(request)

        handle_photo_removal(photo_id, album_name, author)

        return render(request, 'foto_crud/remove_photo.html', {'message': 'Xóa ảnh thành công'})
    except Exception as e:
        logging.error(f"Error in remove_photo: {e}")
        return JsonResponse({'message': 'Không thể xóa ảnh, hãy thử lại'})

def remove_multiple_photos(request):
    try:
        if request.method == 'GET':
            return render(request, 'foto_crud/remove_photo.html')

        photo_ids = request.POST.getlist('photo_ids')
        album_name = request.POST['album']
        author = get_author_from_request(request)

        for photo_id in photo_ids:
            handle_photo_removal(photo_id, album_name, author)

        return render(request, 'foto_crud/remove_photo.html', {'message': 'Xóa ảnh thành công'})
    except Exception as e:
        logging.error(f"Error in remove_multiple_photos: {e}")
        return JsonResponse({'message': 'Không thể xóa những ảnh đã chọn, hãy thử lại'})

def remove_album(request):
    try:
        album_name = request.GET['album']
        author = get_author_from_request(request)

        album_to_remove = Album.objects.filter(album_name=album_name, author=author).first()
        if album_to_remove:
            AlbumPhoto.objects.filter(album=album_to_remove).delete()
            album_to_remove.delete()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        logging.error(f"Error in remove_album: {e}")
        return JsonResponse({'message': 'Không thể xóa album, hãy thử lại'})
    
def search_other_users(request):
    # relative search other username
    try:
        search_username = request.GET['search_username']
        other_users = User.objects.filter(username__icontains=search_username).all()
        other_usernames = [user.username for user in other_users]
        return JsonResponse({'status': 'success', 'other_usernames': other_usernames})
    except Exception as e:
        logging.error(f"Error in search_other_users: {e}")
        return JsonResponse({'message': 'Không thể tìm kiếm người dùng, hãy thử lại'})

