from django.contrib import admin

# Register your models here.
from .models import News, Blogs, Subscriber


admin.site.site_header = "Das And Partners"
admin.site.site_title = "Das And Partners"
admin.site.index_title = "Das And Partners"

class NewsAllField(admin.ModelAdmin):
    list_display = [f.name for f in News._meta.fields]
admin.site.register(News, NewsAllField)

class BlogsAllField(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = [f.name for f in Blogs._meta.fields]
admin.site.register(Blogs, BlogsAllField)

class SubscriberAllField(admin.ModelAdmin):
    list_display = [f.name for f in Subscriber._meta.fields]
admin.site.register(Subscriber, SubscriberAllField)