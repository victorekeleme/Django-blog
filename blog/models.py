from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
from django.utils.text import slugify
from profiles.models import Profile


class Post(models.Model):
    author = models.ForeignKey(Profile, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    content = models.TextField()
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True, max_length=2000)
    image = models.ImageField(default='post.jpg', upload_to='post_pics/')
    published_date = models.DateField(blank=True, null=True)
    category = models.ForeignKey('blog.category', on_delete=models.CASCADE)
    likes = models.ManyToManyField(Profile, blank=True, related_name="post_like")

    def likes_count(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug':self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True, max_length=400)


    class Meta:
        verbose_name_plural = 'Categories'


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog/category_detail.html', kwargs={'slug':self.slug})

class Comments(models.Model):
    author = models.ForeignKey(Profile, related_name="comments", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=1000, blank=True)
    created_on = models.DateField(auto_now=True)


    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug':self.post.slug})

    class Meta:
        verbose_name = "comment"