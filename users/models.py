from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    userid = models.OneToOneField(User, on_delete=models.CASCADE)
    #name = models.CharField(max_length=250)
    #email = models.EmailField(max_length=250, unique= True)
    #password = models.CharField(max_length=100, blank= False, null= False)
    mobile = models.IntegerField(blank=True, null=True)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=50)
    image = models.ImageField(blank=True, upload_to='images/profile_images/',default="images/default_profile.png")

    def __str__(self):
        return self.userid.username


@receiver(post_save,sender=User)
def CreateProfile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(userid=instance)
