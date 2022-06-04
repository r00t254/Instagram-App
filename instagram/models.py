from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField

# Create your models here.  
class Profile(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE)
  profile_image=CloudinaryField('photo')
  bio=models.TextField(blank=True)
  followers=models.IntegerField(default=0)
  following=models.IntegerField(default=0)

  def __str__(self):
    return self.user.username

  @classmethod
  def search_profile(cls, username):
    return User.objects.filter(username=username)

class Image(models.Model):
  image = CloudinaryField('photo')
  caption = models.TextField(blank=True)
  name = models.CharField(max_length=30)
  pub_date = models.DateTimeField(auto_now_add=True)
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  likes=models.ManyToManyField(Profile,related_name="posts")

  def save_image(self):
    self.save()

  def delete_image(self):
    self.delete()

  def __str__(self):
    return self.name
  
  def update_caption(self,updated_caption):
    self.caption= updated_caption
    self.save()

  def likes_num(self):
    self.likes.count()

  @classmethod
  def profile_images(cls,profile):
    return cls.objects.filter(profile=profile)

  class Meta:
    ordering=['-pub_date']

class Comments(models.Model):
  comment=models.TextField()
  pub_date=models.DateTimeField(auto_now_add=True)
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  image=models.ForeignKey(Image, on_delete=models.CASCADE, related_name="comments")
  
  def __str__(self):
    return self.comment

  def save_comment(self):
    self.save()

  def delete_comment(self):
    self.delete()

  @classmethod
  def get_post_comments(cls,image):
    return cls.objects.filter(image=image)

  class Meta:
    ordering=['-pub_date']

class Follow(models.Model):
  posted = models.DateTimeField(auto_now_add=True)
  followed = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="prof_followed")
  follower = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="prof_follower")

def __str__(self):
    return self
