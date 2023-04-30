from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    title = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    video = models.FileField(upload_to='videos')
    videoDescription = models.CharField(max_length=2041, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos_uploaded')
    comments = models.ManyToManyField(User, through='Comment', related_name='videos_commented')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Video_Likes_dislikes(models.Model):
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes_dislikes')
    Like_Dislike_ByUserId = models.IntegerField()
    VideoIsLiked = models.BooleanField()
