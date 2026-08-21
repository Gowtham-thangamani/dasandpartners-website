
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class News(models.Model):
    NEWS_TYPE_CHOICES = [
        ('project', 'Project News'),
        ('general', 'Overall News'),
    ]
    
    FREQUENCY_CHOICES = [
        ('daily', 'Das and Partners Daily'),
        ('weekly', 'Weekly Updates'),
        ('monthly', 'Monthly Updates'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    news_type = models.CharField(max_length=20, choices=NEWS_TYPE_CHOICES, default='general', db_index=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily', db_index=True, help_text="Publication frequency")
    image = models.ImageField(upload_to='news/')
    excerpt = models.TextField(max_length=300, blank=True, help_text="Brief description for news preview")
    content = RichTextField(blank=True, null=True, help_text="Full news content with rich text formatting")
    added_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ['-added_date']

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#148255')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

class Blogs(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='blogs', null=True, blank=True)
    image = models.ImageField(upload_to='blogs/')
    content = RichTextField(blank=True, null=True, help_text="Full blog content with rich text formatting")
    excerpt = models.TextField(max_length=300, blank=True, help_text="Short description for blog preview")
    tags = models.CharField(max_length=255, blank=True, null=True, help_text="Enter comma-separated tags", db_index=True)
    is_published = models.BooleanField(default=True, db_index=True)
    featured = models.BooleanField(default=False, db_index=True)
    read_time = models.PositiveIntegerField(default=5, help_text="Estimated reading time in minutes")
    view_count = models.PositiveIntegerField(default=0)
    added_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.meta_description and self.excerpt:
            self.meta_description = self.excerpt[:160]
        super().save(*args, **kwargs)

    def get_tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['created_date', 'is_published']),
            models.Index(fields=['tags']),
            models.Index(fields=['featured', 'created_date']),
        ]

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
