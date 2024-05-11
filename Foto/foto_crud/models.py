from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    profile_picture = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cookies = models.TextField(blank=True, null=True)

class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    photo_link = models.ImageField()
    upvotes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic_name = models.CharField(max_length=100)

class PhotoTopic(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

class Album(models.Model):
    album_id = models.AutoField(primary_key=True)
    album_name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class AlbumPhoto(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

