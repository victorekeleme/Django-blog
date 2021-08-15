from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
from django.utils.text import slugify


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True)
    image = models.ImageField(default='post.jpg', upload_to='post_pics/')
    created_date = models.DateField(default=timezone.now)
    published_date = models.DateField(blank=True, null=True)
    category = models.ForeignKey('blog.category', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="post_like")

    def likes_count(self):
        return self.likes.count()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug':self.slug})

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True)


    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog/category_detail.html', kwargs={'slug':self.slug})

