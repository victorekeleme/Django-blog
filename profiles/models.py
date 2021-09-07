from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from .utils import get_random_code

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    profile_pic = models.ImageField(default='profiles.png', upload_to='profile_pics/')
    social_links = models.ForeignKey( 'profiles.Socials', related_name='socials', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        ex = False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super(Profile, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.user.username}"

class Socials(models.Model):
    social_name = models.CharField(max_length=200, blank=False)
    url = models.URLField()

    def __str__(self):
        return self.social_name