from django.urls import path

from .views import crud_view, load_view 

urlpatterns = [
    path('', load_view.home, name='home'),
    path('home/', load_view.home, name='home'),
    path('gallery/', load_view.load_photo_topic, name='load_photo_topic'),
    path('profile/', load_view.load_own_photo, name='profile'),
    path('my-albums/', load_view.load_album, name='my-albums'),
    path('upload-photo/', crud_view.upload_photo, name='upload-photo'),
    path('create-album/', crud_view.create_album, name='create-album'),
    path('remove-album/', crud_view.remove_album, name='remove-album'),
    path('save-photo/', crud_view.save_photo, name='save-photo'),
    path('photos-of-album/', load_view.photoOfAlbum, name='photos-of-album'),
    path('search-profile/', load_view.load_user_search, name='search-profile'),
    path('guest-visit/', load_view.load_guest_profile, name='guest-visit'),
    path('photos-of-albums/delete-image/', crud_view.remove_photo, name='remove-photo'),
    path('save-photo/', crud_view.save_photo, name='save-photo'),
    
]