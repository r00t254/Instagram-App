from django.test import TestCase
from .models import Profile,Image,Comments
from django.contrib.auth.models import User

# Create your tests here.
class ImageTestClass(TestCase):
  def setUp(self):
    self.mary=User(username ='mary',email='root254.mary@gmail.com',password='0708202401')
    self.profile=Profile(bio='mybio',profile_image='imageurl',user=self.mary)
    self.tech = Image(image = 'imageurl', name ='tech', caption = 'tech', profile = self.profile)

    self.mary.save()
    self.profile.save()
    self.tech.save_image()

  def tearDown(self):
    Image.objects.all().delete()
  
  def test_instance(self):
    self.assertTrue(isinstance(self.tech, Image))

  def test_save_image(self):
    images=Image.objects.all()
    self.assertTrue(len(images),1)

  def test_delete_image(self):
    images=Image.objects.all()
    self.assertTrue(len(images),1)
    self.tech.delete_image()
    image=Image.objects.all()
    self.assertEqual(len(image),0)

  def test_update_image_caption(self):
    self.tech.update_caption("stunning")
    self.assertEqual(self.tech.caption, 'stunning')

  def test_profile_posts(self):
    images=Image.profile_images(self.profile)
    self.assertEqual(len(images),1)
  

class ProfileTestClass(TestCase):
  def SetUp(self):
    self.user=User(username ='mary',email='root254.mary@gmail.com',password='0708202401')
    self.profile=Profile(bio='mybio',profile_image='imageurl',user='mary')
    self.user.save()
    self.profile.save()

  def tearDown(self):
    Profile.objects.all().delete()
    User.objects.all().delete()

  def test_instance(self):
    self.assertTrue(isinstance(self.user,User))
    self.assertTrue(isinstance(self.profile,Profile))

  def test_search_profile(self):
    user=Profile.search_profile(self.profile)
    self.assertEqual(len(user), 1)

class CommentTestClass(TestCase):
  def setUp(self):
    self.mary=User(username ='mary',email='root254.mary@gmail.com',password='0708202401')
    self.profile=Profile(bio='mybio',profile_image='imageurl',user=self.mary)
    self.tech=Image(image = 'imageurl', name ='tech', caption = 'tech', profile = self.profile)
    self.comment=Comments(image=self.tech, comment='stunning',user=self.mary)

    self.mary.save()
    self.profile.save()
    self.tech.save()
    self.comment.save_comment()


  def tearDown(self):
    Image.objects.all().delete()
    Comments.objects.all().delete()

  def test_instance(self):
    self.assertTrue(isinstance(self.comment, Comments))

  def test_save_comment(self):
    self.comments = Comments(image=self.tech, user=self.mary, comment='test')
    self.comments.save_comment()
    comment = Comments.objects.all()
    self.assertTrue(len(comment),2)

  def test_delete_image(self):
    self.comments = Comments(image=self.tech, user=self.mary, comment='test')
    self.comments.save_comment()
    comments = Comments.objects.all()
    self.assertEqual(len(comments),2)
    self.comments.delete_comment()
    total_comments=Comments.objects.all()
    self.assertEqual(len(total_comments),1)

  def test_get_post(self):
    comments=Comments.get_post_comments(self.tech)
    self.assertEqual(len(comments),1)
