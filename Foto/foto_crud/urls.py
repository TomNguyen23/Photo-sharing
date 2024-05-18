from django.urls import path

from .views import crud_view, load_view 

urlpatterns = [
    path('', load_view.home, name='home'),
    path('home/', load_view.home, name='home'),
    # path('gallery/', foto_crud.gallery, name='gallery'),
    path('profile/', load_view.load_own_photo, name='profile'),
    path('my-albums/', load_view.load_album, name='my-albums'),
    path('upload-photo/', crud_view.upload_photo, name='upload-photo'),
    path('create-album/', crud_view.create_album, name='create-album'),
]