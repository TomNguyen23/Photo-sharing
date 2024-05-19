from ..models import Photo, User, Album, AlbumPhoto

def get_user_from_cookie(cookie):
    return User.objects.filter(cookies=cookie).first()

def get_photos_by_user(user):
    photos = AlbumPhoto.objects.filter(user=user).all()
    return [Photo.objects.filter(photo_id=photo.photo_id).first().photo_link for photo in photos]

def get_author_and_album(author_username, album_name):
    author = User.objects.filter(username=author_username).first()
    album = Album.objects.filter(album_name=album_name, author=author).first()
    return author, album

def get_photos_by_album_and_author(album, author):
    photos = AlbumPhoto.objects.filter(album=album, user=author).all()
    return [Photo.objects.filter(photo_id=photo.photo).first().photo_link for photo in photos]

def get_albums_by_author(author):
    albums = Album.objects.filter(author=author).all()
    return [album.album_name for album in albums]