from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save,pre_save

class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Lead(models.Model):
    
    SOURCE_CHOICES = (
        ('YT', 'YouTube'),
        ('GOOG', 'Google'),
        ('NL', 'Newsletter'),
        ('YAH', 'Yahoo')
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)

    phoned = models.BooleanField(default=False)
    source = models.CharField(max_length=5, choices= SOURCE_CHOICES)

    profile_pic = models.ImageField(blank=True, null=True)
    special_files = models.FileField(blank=True, null=True)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", related_name='leads', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=30)      #NEW, CONTACTED, CONVERTED, UNCONVERTED
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


import pyqrcode
import png
import os

def post_agent_created_qr(sender, instance, created, **kwargs):
    if created:
        user = instance
        print(user.user)
        qr = pyqrcode.create(str(user.user))
        qr_path = f"media/agents/{str(user.user)}/"
        if (os.path.isdir(qr_path)):
            qr.svg(qr_path, scale=8)
        else:
            os.chdir("media/agents/")
            os.makedirs(f"{str(user.user)}")
            qr.svg(f"{str(user.user)}/qr.svg", scale=8, module_color="#6600FF")

post_save.connect(post_agent_created_qr, sender=Agent)

def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)

post_save.connect(post_user_created_signal, sender=User)