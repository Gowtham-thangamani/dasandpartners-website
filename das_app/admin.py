from django.contrib import admin
from .models import News, Blogs, Subscriber, BlogCategory

admin.site.site_header = "Das And Partners"
admin.site.site_title = "Das And Partners"
admin.site.index_title = "Das And Partners"

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'news_type', 'frequency', 'created_date', 'added_date']
    list_filter = ['news_type', 'frequency', 'created_date', 'added_date']
    search_fields = ['title', 'excerpt']
    date_hierarchy = 'created_date'
    list_editable = ['news_type', 'frequency']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'news_type', 'frequency', 'excerpt')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Dates', {
            'fields': ('added_date',)
        }),
    )

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'featured', 'view_count', 'created_date']
    list_filter = ['category', 'is_published', 'featured', 'created_date', 'tags']
    search_fields = ['title', 'content', 'tags', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published', 'featured']
    list_per_page = 25
    date_hierarchy = 'created_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'excerpt')
        }),
        ('Content', {
            'fields': ('content', 'image', 'tags')
        }),
        ('Publishing', {
            'fields': ('is_published', 'featured', 'read_time', 'added_date')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']
    list_filter = ['subscribed_at']
    search_fields = ['email']
    date_hierarchy = 'subscribed_at'
