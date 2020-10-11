from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings
from autoslug import AutoSlugField

# Create your models here.
#creates profile model
class Profile(models.Model):
    #stores user/deletes profile on deletion of user
    user=models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    #stores display name
    display_name=models.CharField(max_length=50)
    #stores first name
    first_name=models.CharField(max_length=50)
    #stores last name
    last_name=models.CharField(max_length=50)
    #stores industry of expertise
    industry=models.CharField(max_length=50)
    #stores occupational title, allows to be blank
    occupational_title=models.CharField(max_length=50, blank=True)
    #stores specialization, allows to be blank
    specialization=models.CharField(max_length=50, blank=True)
    #stores date joined
    date_joined=models.DateTimeField()
    #stores profile pic and save to 'profile_pics' dir
    profile_pic=models.ImageField(default='default.png',upload_to='profile_pics')
    #stores slug (end of url for profiles)
    slug=AutoSlugField(populate_from='user')
    #stores bio, allows it to be left blank
    bio=models.CharField(max_length=500, blank=True)
    #stores friends. Every user can have multiple friends/can be friends to mult ppl
    friends=models.ManyToManyField("Profile", blank=True)

    #tells Django Admin how to store our models. Use username 
    def __str__(self):
        return str(self.user.username)

    #creates absolute url format for slugs
    def get_absolute_url(self):
        return "/users/{}".format(self.slug)

#creates profile if user is created
def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    #if user is created
    if created:
        #create a profile
        try:
            Profile.objects.create(user=instance)
        #otherwise, FORGET ABOUT IT
        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)


#create FriendRequest model
class FriendRequest(models.Model):
    #defines who the friend request is being sent to
    #if the user who the friend request is being sent to, is deleted,
    #delete the friend request too 
    to_user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name="to_user", on_delete=models.CASCADE)
    #defines who is sending the request
    #if the sender is deleted as a user from the system,
    #delete the sent friend request also
    from_user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name="from_user", on_delete=models.CASCADE)
    #stores timestamp of friend request
    timestamp = models.DateTimeField(auto_now_add=True)

    #tells django admin how to store friend requests model:
    #"from user1 to user"
    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)

class Project(models.Model):
    #date started
    date_started = models.DateTimeField(null=True)
    project_name = models.CharField(max_length = 250)
    project_synopsis = models.CharField(max_length = 1000)
    project_description = models.CharField(max_length = 100000)
    project_collaborators = models.ManyToManyField("Project", blank=True)
    by_user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name="by_user", on_delete=models.CASCADE)
