#!/usr/bin/env python3
"""
Export data from current hosting for migration to VPS

Run this on your CURRENT hosting or locally if you have database access

Usage:
    python3 export_current_data.py
"""

import os
import sys
import django
import csv
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'das_project.settings')
django.setup()

from das_app.models import Blogs, News, BlogCategory

def export_blogs():
    """Export all blogs to CSV"""
    filename = f'blogs_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    blogs = Blogs.objects.all().order_by('-added_date')
    
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'id', 'title', 'slug', 'category', 'excerpt', 'content',
            'tags', 'is_published', 'featured', 'read_time', 'added_date',
            'image_url'
        ])
        
        # Data
        count = 0
        for blog in blogs:
            try:
                writer.writerow([
                    blog.id,
                    blog.title,
                    blog.slug,
                    blog.category.name if blog.category else '',
                    blog.excerpt,
                    blog.content,
                    blog.tags,
                    blog.is_published,
                    blog.featured,
                    blog.read_time,
                    blog.added_date.strftime('%Y-%m-%d %H:%M:%S'),
                    blog.image.url if blog.image else ''
                ])
                count += 1
            except Exception as e:
                print(f"Error exporting blog '{blog.title}': {str(e)}")
        
        print(f"✅ Exported {count} blogs to {filename}")
    
    return filename


def export_news():
    """Export all news to CSV"""
    filename = f'news_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    news = News.objects.all().order_by('-added_date')
    
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'id', 'title', 'slug', 'news_type', 'frequency', 'excerpt',
            'content', 'added_date', 'image_url'
        ])
        
        # Data
        count = 0
        for news_item in news:
            try:
                writer.writerow([
                    news_item.id,
                    news_item.title,
                    news_item.slug,
                    news_item.news_type if hasattr(news_item, 'news_type') else 'general',
                    news_item.frequency if hasattr(news_item, 'frequency') else 'daily',
                    news_item.excerpt if hasattr(news_item, 'excerpt') else '',
                    news_item.content if hasattr(news_item, 'content') else '',
                    news_item.added_date.strftime('%Y-%m-%d %H:%M:%S'),
                    news_item.image.url if news_item.image else ''
                ])
                count += 1
            except Exception as e:
                print(f"Error exporting news '{news_item.title}': {str(e)}")
        
        print(f"✅ Exported {count} news articles to {filename}")
    
    return filename


def export_categories():
    """Export blog categories"""
    filename = f'categories_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    categories = BlogCategory.objects.all()
    
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow(['id', 'name', 'description'])
        
        # Data
        count = 0
        for category in categories:
            writer.writerow([
                category.id,
                category.name,
                category.description if hasattr(category, 'description') else ''
            ])
            count += 1
        
        print(f"✅ Exported {count} categories to {filename}")
    
    return filename


def create_image_list():
    """Create list of all image URLs to download"""
    filename = f'images_list_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    
    images = []
    
    # Blog images
    for blog in Blogs.objects.all():
        if blog.image:
            images.append(f"BLOG|{blog.image.url}|{blog.slug}")
    
    # News images
    for news in News.objects.all():
        if news.image:
            images.append(f"NEWS|{news.image.url}|{news.slug}")
    
    with open(filename, 'w') as f:
        for img in images:
            f.write(img + '\n')
    
    print(f"✅ Created image list with {len(images)} images: {filename}")
    return filename


def main():
    """Main export function"""
    print("=" * 60)
    print("📦 EXPORTING DATA FROM CURRENT HOSTING")
    print("=" * 60)
    print()
    
    try:
        # Export blogs
        print("📝 Exporting blogs...")
        blogs_file = export_blogs()
        print()
        
        # Export news
        print("📰 Exporting news...")
        news_file = export_news()
        print()
        
        # Export categories
        print("📂 Exporting categories...")
        cat_file = export_categories()
        print()
        
        # Create image list
        print("🖼️  Creating image list...")
        img_file = create_image_list()
        print()
        
        print("=" * 60)
        print("✅ EXPORT COMPLETE!")
        print("=" * 60)
        print()
        print("Files created:")
        print(f"  - {blogs_file}")
        print(f"  - {news_file}")
        print(f"  - {cat_file}")
        print(f"  - {img_file}")
        print()
        print("Next steps:")
        print("1. Download these files to your Mac")
        print("2. Upload to VPS:")
        print(f"   scp {blogs_file} root@VPS_IP:/var/www/dasandpartners/")
        print(f"   scp {news_file} root@VPS_IP:/var/www/dasandpartners/")
        print("3. Import using import_content.py on VPS")
        print()
        
    except Exception as e:
        print(f"❌ Error during export: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()





