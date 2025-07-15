
from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.utils import timezone
from django.utils.text import slugify

class News(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='dasandpartners/news/')
    added_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "New"
        verbose_name_plural = "News"

class Blogs(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='dasandpartners/blogs/')
    content = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True, help_text="Enter comma-separated tags")
    added_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"





class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)