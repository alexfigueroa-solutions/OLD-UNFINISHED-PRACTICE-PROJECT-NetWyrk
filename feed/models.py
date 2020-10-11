from django.db import models

# Create your models here.
#creates a user in the db

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    
    pic = models.ImageField(upload_to = 'path/to/img', null = True)
    date_posted = models.DateTimeField(default = timezone.now)
    #delete post on deletion of user
    user_name = models.ForeignKey(User, on_delete = models.CASCADE)
    tags = models.CharField(max_length = 100, blank = True)

    #define posts by description in django admin
    def __str__(self):
        return self.description
    
    #gets url to post
    def get_absolute_url(self):
        return reverse('post-detail', kwargs = {'pk':self.pk})
    
#comments class
class Comments(models.Model):
    #delete comments on deletion of post
    #brings up post as a detail of the comment 
    post = models.ForeignKey(Post, related_name = 'details', on_delete = models.CASCADE)
    #on deletion of user, delete comments
    #brings up username as a detail of the comment
    username = models.ForeignKey(User, related_name = 'details', on_delete = models.CASCADE)
    comment = models.CharField(max_length = 100000)
    comment_date =models.DateTimeField(default = timezone.now)

#creates class for liking posts
class Like(models.Model):
    #user that liked the photo, stores under 'likes'
    user = models.ForeignKey(User, related_name = "likes", on_delete = models.CASCADE)
    #post that user liked. 
    post = models.ForeignKey(Post, related_name = 'likes', on_delete = models.CASCADE)
    