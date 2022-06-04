from django.db import models
from django.db.models import fields
from .models import Image,Follow,Profile,Comments
from django.forms import  ModelForm

class FollowForm(ModelForm):
  class Meta:
    model = Follow
    exclude = ['followed','follower']

class UnfollowForm(ModelForm):
  class Meta:
    model = Follow
    exclude = ['followed','follower']

class CreateProfileForm(ModelForm):
  class Meta:
    model = Profile
    exclude = ['user','followers','following']

class UpdateProfile(ModelForm):
  class Meta:
    model = Profile
    fields = ['bio','profile_image']

class CreatePost(ModelForm):
  class Meta:
    model = Image
    fields = ['image','caption','name']