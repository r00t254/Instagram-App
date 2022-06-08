from django import forms
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,Http404
from .models import Profile,Follow,Image,Comments
from django.contrib.auth.models import User
from .form import UnfollowForm,FollowForm,CreateProfileForm,UpdateProfile,CreatePost
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .email import send_welcome_email

# Create your views here.
# @login_required
def index(request):
  # current_user=request.user
  
  # try:
  #   profile= Profile.objects.get(user=current_user)
  #   print(current_user)
  # except Profile.DoesNotExist:
  #   raise Http404()

  # index_timeline=[]
  # images = Image.objects.filter(profile=profile)
  # for image in images:
  #   index_timeline.append(image.id)

  # followers_posts=Follow.objects.filter(follower=profile)
  # for follower in followers_posts:
  #   followed_profiles=follower.followed
  #   followed_images=Image.profile_images(followed_profiles)
  #   for images in followed_images:
  #     index_timeline.append(images.id)
  # timeline_images=Image.objects.filter(pk__in=index_timeline).order_by('-pub_date')

  all_profiles=Profile.objects.all()
  comments=Comments.objects.all()[:5]
  count=comments.count()
  follow_suggestions=Profile.objects.all()[:6]
  title = "Instagram-App"

  return render(request, 'instagram/index.html')
  # return render(request,'instagram/index.html',{"all_profiles":all_profiles,"title":title,"profile":profile,"timeline_images":timeline_images,"follow_suggestions":follow_suggestions,"image_comments":comments})
  
@login_required
def welcome_mail(request):
  user=request.user
  email=user.email
  name=user.username
  send_welcome_email(name,email)
  return redirect(create_profile)

@login_required
def search(request):
  if 'user' in request.GET and request.GET['user']:
    searched_profile = request.GET.get("user")
    try:
      user = Profile.search_profile(searched_profile)
      profile_id = user[0].id
    except User.DoesNotExist:
      raise Http404()
    current_user = request.user
    try:
      profile = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
      raise Http404()
    try:
      prof_follower = Profile.objects.get(user=current_user)
    except Profile.DoesNotExist:
      raise Http404()
    try:
      prof_followed = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
      raise Http404()

    if request.method == 'POST':
      if 'follow' in request.POST:
        form = FollowForm(request.POST)
        if form.is_valid():
          new_followed = form.save(commit=False)
          new_followed.followed = prof_followed
          new_followed.follower = prof_follower
          new_followed.save()
          user_following = Follow.objects.filter(followed=prof_followed)
          following_stats = len(user_following)
          prof_followed.followers = following_stats
          prof_followed.save()

          user_followers = Follow.objects.filter(follower=prof_follower)
          followers_stats = len(user_followers)
          prof_follower.following = followers_stats
          prof_follower.save()

        return HttpResponseRedirect(f'/profile/{profile_id}')

      elif 'unfollow' in request.POST:
        form = UnfollowForm(request.POST)
        if form.is_valid():
          new_unfollow = form.save(commit=False)
          new_unfollow= Follow.objects.filter(followed = prof_followed, follower = prof_follower)
          new_unfollow.delete()

          user_following = Follow.objects.filter(followed=prof_followed)
          following_stats = len(user_following)
          prof_followed.followers = following_stats
          prof_followed.save()

          user_followers = Follow.objects.filter(follower=prof_follower)
          followers_stats = len(user_followers)
          prof_follower.following = followers_stats
          prof_follower.save()

        return HttpResponseRedirect(f'/profile/{profile_id}')

    else:
      follow_form = FollowForm()
      unfollow_form = UnfollowForm()

    images = Image.profile_images(profile=profile).order_by('-pub_date')

    post = len(images)

    is_following = Follow.objects.filter(
        followed=prof_followed, follower=prof_follower)

    if is_following:
      return render(request, 'profile/profile.html', {"profile": profile, "post": post, "images": images, "unfollow_form": unfollow_form})
    return render(request, 'profile/profile.html', {"profile": profile, "images": images, "post": post, "follow_form": follow_form, "search":searched_profile})

  else:
    not_searched = "No user searched"
  return render(request, 'profile/profile.html', {"not_searched": not_searched})


@login_required
def profile(request,profile_id):
  current_user = request.user
  try:
    profile=Profile.objects.get(id=profile_id)
  except Profile.DoesNotExist:
    raise Http404()
  try:
    prof_follower=Profile.objects.get(user=current_user)
  except Profile.DoesNotExist:
    raise Http404()
  try:
    prof_followed=Profile.objects.get(id=profile_id)
  except Profile.DoesNotExist:
    raise Http404()

  if request.method == 'POST':
    if 'follow' in request.POST:
      form = FollowForm(request.POST)
      if form.is_valid():
        new_followed = form.save(commit=False)
        new_followed.followed = prof_followed
        new_followed.follower = prof_follower
        new_followed.save()
        user_following = Follow.objects.filter(followed=prof_followed)
        following_stats = len(user_following)
        prof_followed.followers = following_stats
        prof_followed.save()

        user_followers = Follow.objects.filter(follower=prof_follower)
        followers_stats = len(user_followers)
        prof_follower.following = followers_stats
        prof_follower.save()
        
      return HttpResponseRedirect(f'/profile/{profile_id}')

    elif 'unfollow' in request.POST:
      form = UnfollowForm(request.POST)
      if form.is_valid():
        new_unfollow = form.save(commit=False)
        new_unfollow= Follow.objects.filter(followed = prof_followed, follower = prof_follower)
        new_unfollow.delete()

        user_following = Follow.objects.filter(followed=prof_followed)
        following_stats = len(user_following)
        prof_followed.followers = following_stats
        prof_followed.save()

        user_followers = Follow.objects.filter(follower=prof_follower)
        followers_stats = len(user_followers)
        prof_follower.following = followers_stats
        prof_follower.save()

      return HttpResponseRedirect(f'/profile/{profile_id}')

  else:
    follow_form=FollowForm()
    unfollow_form=UnfollowForm()

  images=Image.profile_images(profile=profile).order_by('-pub_date')

  post=len(images)

  is_following=Follow.objects.filter(followed=prof_followed,follower=prof_follower)

  if is_following:
    return render(request,'profile/profile.html',{"profile":profile,"post":post,"images":images,"unfollow_form":unfollow_form})
  return render(request,'profile.html',{"profile":profile,"images":images,"post":post,"follow_form":follow_form,})


@login_required
def comment(request,image_id):
  image=Image.objects.get(pk=image_id)
  comments=request.GET.get("comments")
  current_user=request.user
  comment=Comments(image=image,comment=comments,user=current_user)
  comment.save_comment()

  return redirect('home')

@login_required
def create_profile(request):
  current_user=request.user
  if request.method == 'POST':
    form = CreateProfileForm(request.POST,request.FILES)
    if form.is_valid():
      profile = form.save(commit=False)
      profile.user = current_user
      profile.save()
    return HttpResponseRedirect('/')
  else:
    form = CreateProfileForm()
  return render(request,'create_profile.html',{"form":form})

@login_required
def like_post(request,image_id):
  image = Image.objects.get(pk=image_id)
  is_liked=False
  user=request.user
  try:
    profile=Profile.objects.get(user=user)
  except Profile.DoesNotExist:
    raise Http404()
  if image.likes.filter(id=profile.id).exists():
    image.likes.remove(profile)
    is_liked=False
  else:
    image.likes.add(profile)
    is_liked=True
  return HttpResponseRedirect(reverse('home'))
  
@login_required
def update_profile(request):
  user=request.user
  if request.method == 'POST':
    form=UpdateProfile(request.POST,request.FILES)
    if form.is_valid():
      profile_image = form.cleaned_data['profile_image']
      bio = form.cleaned_data['bio']
      update_prof=Profile(profile_image=profile_image,bio=bio,user=user)
      update_prof.save()
    return redirect('profile')
  else:
    form = UpdateProfile()
  return render(request, '.html',{"form":form})

@login_required
def upload_post(request):
  user=request.user
  try:
    profile=Profile.objects.get(user=user)
  except Profile.DoesNotExist:
    raise Http404()
  if request.method == 'POST':
    form = CreatePost(request.POST,request.FILES)
    if form.is_valid():
      new_post=form.save(commit=False)
      new_post.profile = profile
      new_post.save()
    return redirect(reverse('profile'))
  else:
    form = CreatePost()
  return render(request,'create_post.html',{"form":form})

@login_required
def single_post(request,image_id):
  try:
    image=Image.objects.get(id=image_id)
    return render(request,'single-post.html',{"image":image})
  except Image.DoesNotExist:
    raise Http404()
  
  
def login(request):
    """
      if request.method == 'POST':
      print(request.POST) 
      """
    if form_is_valid:

   
      
      return redirect('profile')
    return render(request, 'registration/login.html')
  
   
def registration(request):
    """
      if request.method == 'POST':
      print(request.POST) 
      """
      
    return render(request, 'django_registration/registration_form.html')
