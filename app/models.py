from django.db import models
from django.db.models.fields import NullBooleanField
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from embed_video.fields import EmbedVideoField
# Create your models here.

SUBSCRIPTION =(
  ('F', 'FREE'),
  ('M','MONTHLY'),
  ('Y','YEARLY'),
 )

class Profile(models.Model):
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 is_pro = models.BooleanField(default=False)
 pro_expiery_date = models.DateTimeField(null=True,blank=True)
 subscription_type = models.CharField(max_length=100, choices=SUBSCRIPTION, default="FREE")
 
 def __str__(self):
   return str(self.user)

class Video(models.Model):
 video_name = models.CharField(max_length=200)
 video_desc = RichTextField()
 is_Premium = models.BooleanField(default=False)
 video_image = models.ImageField(upload_to='video')
 slug = models.SlugField(blank=True)
 video = models.FileField(upload_to='videos/')
 
 def save(self, *args, **kwargs):
  self.slug = slugify(self.video_name)
  super(Video, self).save( *args, *kwargs)

 def __str__(self):
  return self.video_name

class Contact(models.Model):
 name = models.CharField(max_length=122)
 email = models.CharField(max_length=122)
 phone = models.CharField(max_length=122)
 desc = models.TextField()

 def __str__(self):
     return self.name