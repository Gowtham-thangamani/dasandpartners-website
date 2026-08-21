# 📦 Bulk Content Import Guide

## 🎯 How to Import 100s of Blogs & News at Once

Perfect for migrating existing content or bulk uploading!

---

## 📋 Method 1: CSV Import (Easiest)

### Step 1: Prepare Your CSV File

Create a file called `blogs_import.csv`:

```csv
title,slug,category,excerpt,content,tags,is_published,featured,read_time,added_date
"MEP Engineering in Dubai","mep-engineering-dubai","Engineering","Learn about MEP services...","<h2>Introduction</h2><p>MEP engineering involves...</p>","mep,dubai,engineering",true,false,5,"2025-10-01 10:00:00"
"BIM for Construction","bim-construction","Technology","BIM overview...","<h2>What is BIM?</h2><p>Building Information Modeling...</p>","bim,construction",true,true,7,"2025-10-02 10:00:00"
```

For news, create `news_import.csv`:

```csv
title,slug,news_type,frequency,excerpt,content,added_date
"Project Milestone Achieved","project-milestone","project","daily","We completed Phase 1...","<p>Today we successfully completed...</p>","2025-10-01 09:00:00"
"Weekly Update Oct 1-7","weekly-update-oct1","general","weekly","This week's highlights...","<h2>Week in Review</h2><p>This week we...</p>","2025-10-07 17:00:00"
```

### Step 2: Create Import Script

Create `import_content.py` in your project root:

```python
import csv
import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'das_project.settings')
django.setup()

from das_app.models import Blogs, News, BlogCategory

def import_blogs(csv_file):
    """Import blogs from CSV"""
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        
        for row in reader:
            try:
                # Get or create category
                category = None
                if row.get('category'):
                    category, _ = BlogCategory.objects.get_or_create(
                        name=row['category']
                    )
                
                # Parse date
                added_date = datetime.strptime(row['added_date'], '%Y-%m-%d %H:%M:%S')
                
                # Create blog
                blog, created = Blogs.objects.get_or_create(
                    slug=row['slug'],
                    defaults={
                        'title': row['title'],
                        'category': category,
                        'excerpt': row['excerpt'],
                        'content': row['content'],
                        'tags': row.get('tags', ''),
                        'is_published': row.get('is_published', 'true').lower() == 'true',
                        'featured': row.get('featured', 'false').lower() == 'true',
                        'read_time': int(row.get('read_time', 5)),
                        'added_date': added_date,
                    }
                )
                
                if created:
                    count += 1
                    print(f"✓ Created: {blog.title}")
                else:
                    print(f"- Exists: {blog.title}")
                    
            except Exception as e:
                print(f"✗ Error with '{row.get('title', 'Unknown')}': {str(e)}")
        
        print(f"\n✅ Imported {count} blogs successfully!")

def import_news(csv_file):
    """Import news from CSV"""
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        
        for row in reader:
            try:
                # Parse date
                added_date = datetime.strptime(row['added_date'], '%Y-%m-%d %H:%M:%S')
                
                # Create news
                news, created = News.objects.get_or_create(
                    slug=row['slug'],
                    defaults={
                        'title': row['title'],
                        'news_type': row.get('news_type', 'general'),
                        'frequency': row.get('frequency', 'daily'),
                        'excerpt': row['excerpt'],
                        'content': row['content'],
                        'added_date': added_date,
                    }
                )
                
                if created:
                    count += 1
                    print(f"✓ Created: {news.title}")
                else:
                    print(f"- Exists: {news.title}")
                    
            except Exception as e:
                print(f"✗ Error with '{row.get('title', 'Unknown')}': {str(e)}")
        
        print(f"\n✅ Imported {count} news articles successfully!")

# Run imports
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python import_content.py [blogs|news] <csv_file>")
        sys.exit(1)
    
    content_type = sys.argv[1]
    csv_file = sys.argv[2]
    
    if content_type == 'blogs':
        import_blogs(csv_file)
    elif content_type == 'news':
        import_news(csv_file)
    else:
        print("Invalid type. Use 'blogs' or 'news'")
```

### Step 3: Run Import

```bash
cd "/Users/haider/Desktop/new backup/dasandpartners-django-main"

# Import blogs
python3 import_content.py blogs blogs_import.csv

# Import news
python3 import_content.py news news_import.csv
```

---

## 📦 Method 2: JSON Import (Advanced)

### Export Existing Data
```bash
# Export all blogs
python3 manage.py dumpdata das_app.Blogs --indent 2 > blogs_export.json

# Export all news
python3 manage.py dumpdata das_app.News --indent 2 > news_export.json
```

### Edit JSON & Import
```bash
# Edit the JSON file with your content
# Then import:
python3 manage.py loaddata blogs_export.json
python3 manage.py loaddata news_export.json
```

---

## 🖼️ Method 3: Bulk Image Upload

### Upload Images via SFTP/SCP

```bash
# Upload blog images
scp /path/to/images/*.jpg user@vps-ip:/var/www/dasandpartners/media/blogs/

# Upload news images
scp /path/to/images/*.jpg user@vps-ip:/var/www/dasandpartners/media/news/

# Or use FileZilla for GUI upload
```

---

## 🚀 Method 4: Django Admin Bulk Import

### Install Django Import-Export

```bash
pip install django-import-export
```

Add to `settings.py`:
```python
INSTALLED_APPS = [
    # ... existing apps
    'import_export',
]
```

Update `admin.py`:
```python
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class BlogResource(resources.ModelResource):
    class Meta:
        model = Blogs

@admin.register(Blogs)
class BlogsAdmin(ImportExportModelAdmin):
    resource_class = BlogResource
    # ... existing config
```

### Use Django Admin Interface

1. Go to `/admin/`
2. Click "Blogs" → "Import"
3. Upload your CSV/Excel file
4. Preview → Confirm → Done! ✅

---

## 📊 Quick Import Templates

### Blog CSV Template
```csv
title,slug,category,excerpt,content,tags,is_published,featured,read_time,added_date,image
"Title 1","title-1","Engineering","Short desc...","<p>Content...</p>","tag1,tag2",true,false,5,"2025-10-01 10:00:00",""
"Title 2","title-2","Technology","Short desc...","<p>Content...</p>","tag3,tag4",true,true,7,"2025-10-02 10:00:00",""
```

### News CSV Template
```csv
title,slug,news_type,frequency,excerpt,content,added_date,image
"Daily Update 1","daily-1","project","daily","Quick update...","<p>Today we...</p>","2025-10-01 09:00:00",""
"Weekly Summary","weekly-1","general","weekly","Week review...","<h2>This Week</h2><p>...</p>","2025-10-07 17:00:00",""
```

---

## 💡 Best Practices

### Before Bulk Import

1. ✅ **Backup database:**
   ```bash
   cp db.sqlite3 db.sqlite3.backup
   ```

2. ✅ **Test with 5-10 items first**

3. ✅ **Prepare all images in advance**

4. ✅ **Use consistent naming:**
   - Slugs: lowercase-with-hyphens
   - Images: descriptive-name.jpg

### During Import

1. ✅ **Monitor server resources**
   ```bash
   htop  # Watch CPU/RAM usage
   ```

2. ✅ **Import in batches:**
   - 100 posts at a time
   - Wait 1-2 minutes between batches

3. ✅ **Check logs for errors**

### After Import

1. ✅ **Verify content:**
   ```bash
   python manage.py shell
   >>> from das_app.models import Blogs, News
   >>> Blogs.objects.count()
   >>> News.objects.count()
   ```

2. ✅ **Test sample posts:**
   - Visit blog/news pages
   - Check images load
   - Verify links work

3. ✅ **Create backup:**
   ```bash
   python manage.py dumpdata > backup_after_import.json
   ```

---

## 🎯 Bulk Upload Workflow

### For 500+ Posts

```
Day 1: Preparation
├── Prepare CSV files
├── Prepare all images
├── Test import with 10 posts
└── Verify everything works

Day 2: Import Content
├── Batch 1: 100 posts (morning)
├── Verify batch 1
├── Batch 2: 100 posts (afternoon)
├── Verify batch 2
└── Continue...

Day 3: Import Images
├── Upload all images to /media/
├── Link images to posts
└── Verify all images show

Day 4: Verification
├── Check all posts
├── Test search functionality
├── Verify SEO fields
└── Create backup
```

---

## 🔧 Troubleshooting

### Import Errors

**"Slug already exists"**
```
Solution: Use unique slugs or update existing
```

**"Image not found"**
```
Solution: Upload images first, then import content
```

**"Timeout during import"**
```
Solution: 
- Import in smaller batches (50 instead of 100)
- Increase timeout in settings.py:
  DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB
```

---

## 📈 Expected Import Performance

### On Your 4 vCPU / 8GB VPS:

```
100 blogs (text only): ~1-2 minutes
100 blogs (with images): ~3-5 minutes
500 news articles: ~5-10 minutes
1000 total posts: ~15-20 minutes

Compared to 1 vCPU / 1GB:
100 blogs: ~10-15 minutes
500 news: ~30-40 minutes
1000 total: ~60-90 minutes

Your VPS is 4-5x FASTER for bulk imports! ✅
```

---

## 🎊 Summary

### Bulk Import Options:

| Method | Difficulty | Speed | Best For |
|--------|-----------|-------|----------|
| CSV Script | Easy | Fast | Structured data |
| JSON Import | Medium | Fast | Existing Django data |
| Django Admin | Easiest | Medium | Non-technical users |
| Direct Database | Hard | Fastest | Developers only |

---

**Your 4 vCPU / 8GB VPS will handle bulk imports beautifully!** 🚀

Want me to create more specific import scripts for your content? Let me know! 🎉





