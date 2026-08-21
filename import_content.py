#!/usr/bin/env python3
"""
Bulk Content Import Script for Das and Partners
Import blogs and news from CSV files

Usage:
    python3 import_content.py blogs blogs_import.csv
    python3 import_content.py news news_import.csv
"""

import csv
import os
import sys
import django
from datetime import datetime
from pathlib import Path

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'das_project.settings')
django.setup()

from das_app.models import Blogs, News, BlogCategory
from django.utils.text import slugify
from django.core.files import File


def import_blogs(csv_file):
    """Import blogs from CSV file"""
    if not os.path.exists(csv_file):
        print(f"❌ Error: File '{csv_file}' not found!")
        return
    
    print("=" * 60)
    print("📦 IMPORTING BLOGS")
    print("=" * 60)
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count_created = 0
        count_existed = 0
        count_errors = 0
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is 1)
            try:
                # Validate required fields
                if not row.get('title'):
                    print(f"⚠️  Row {row_num}: Missing title, skipping...")
                    count_errors += 1
                    continue
                
                # Generate slug if not provided
                slug = row.get('slug', '').strip()
                if not slug:
                    slug = slugify(row['title'])
                
                # Get or create category
                category = None
                if row.get('category'):
                    category, _ = BlogCategory.objects.get_or_create(
                        name=row['category'].strip(),
                        defaults={'description': f'{row["category"]} category'}
                    )
                
                # Parse date
                added_date = None
                if row.get('added_date'):
                    try:
                        added_date = datetime.strptime(
                            row['added_date'].strip(), 
                            '%Y-%m-%d %H:%M:%S'
                        )
                    except ValueError:
                        try:
                            added_date = datetime.strptime(
                                row['added_date'].strip(), 
                                '%Y-%m-%d'
                            )
                        except ValueError:
                            print(f"⚠️  Row {row_num}: Invalid date format, using current date")
                            added_date = datetime.now()
                else:
                    added_date = datetime.now()
                
                # Parse boolean fields
                is_published = row.get('is_published', 'true').lower() in ['true', '1', 'yes']
                featured = row.get('featured', 'false').lower() in ['true', '1', 'yes']
                
                # Parse read time
                try:
                    read_time = int(row.get('read_time', 5))
                except ValueError:
                    read_time = 5
                
                # Create or update blog
                blog, created = Blogs.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'title': row['title'].strip(),
                        'category': category,
                        'excerpt': row.get('excerpt', '').strip(),
                        'content': row.get('content', '').strip(),
                        'tags': row.get('tags', '').strip(),
                        'is_published': is_published,
                        'featured': featured,
                        'read_time': read_time,
                        'added_date': added_date,
                    }
                )
                
                if created:
                    count_created += 1
                    print(f"✅ Created: {blog.title}")
                else:
                    count_existed += 1
                    print(f"🔄 Updated: {blog.title}")
                    
            except Exception as e:
                count_errors += 1
                print(f"❌ Error in row {row_num} ('{row.get('title', 'Unknown')}'): {str(e)}")
    
    print("\n" + "=" * 60)
    print("📊 IMPORT SUMMARY")
    print("=" * 60)
    print(f"✅ Created:  {count_created} blogs")
    print(f"🔄 Updated:  {count_existed} blogs")
    print(f"❌ Errors:   {count_errors}")
    print(f"📝 Total:    {count_created + count_existed + count_errors}")
    print("=" * 60)


def import_news(csv_file):
    """Import news from CSV file"""
    if not os.path.exists(csv_file):
        print(f"❌ Error: File '{csv_file}' not found!")
        return
    
    print("=" * 60)
    print("📰 IMPORTING NEWS")
    print("=" * 60)
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count_created = 0
        count_existed = 0
        count_errors = 0
        
        for row_num, row in enumerate(reader, start=2):
            try:
                # Validate required fields
                if not row.get('title'):
                    print(f"⚠️  Row {row_num}: Missing title, skipping...")
                    count_errors += 1
                    continue
                
                # Generate slug if not provided
                slug = row.get('slug', '').strip()
                if not slug:
                    slug = slugify(row['title'])
                
                # Parse date
                added_date = None
                if row.get('added_date'):
                    try:
                        added_date = datetime.strptime(
                            row['added_date'].strip(), 
                            '%Y-%m-%d %H:%M:%S'
                        )
                    except ValueError:
                        try:
                            added_date = datetime.strptime(
                                row['added_date'].strip(), 
                                '%Y-%m-%d'
                            )
                        except ValueError:
                            print(f"⚠️  Row {row_num}: Invalid date format, using current date")
                            added_date = datetime.now()
                else:
                    added_date = datetime.now()
                
                # Validate news_type
                news_type = row.get('news_type', 'general').lower()
                if news_type not in ['project', 'general']:
                    print(f"⚠️  Row {row_num}: Invalid news_type '{news_type}', using 'general'")
                    news_type = 'general'
                
                # Validate frequency
                frequency = row.get('frequency', 'daily').lower()
                if frequency not in ['daily', 'weekly', 'monthly']:
                    print(f"⚠️  Row {row_num}: Invalid frequency '{frequency}', using 'daily'")
                    frequency = 'daily'
                
                # Create or update news
                news, created = News.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'title': row['title'].strip(),
                        'news_type': news_type,
                        'frequency': frequency,
                        'excerpt': row.get('excerpt', '').strip(),
                        'content': row.get('content', '').strip(),
                        'added_date': added_date,
                    }
                )
                
                if created:
                    count_created += 1
                    print(f"✅ Created: {news.title}")
                else:
                    count_existed += 1
                    print(f"🔄 Updated: {news.title}")
                    
            except Exception as e:
                count_errors += 1
                print(f"❌ Error in row {row_num} ('{row.get('title', 'Unknown')}'): {str(e)}")
    
    print("\n" + "=" * 60)
    print("📊 IMPORT SUMMARY")
    print("=" * 60)
    print(f"✅ Created:  {count_created} news articles")
    print(f"🔄 Updated:  {count_existed} news articles")
    print(f"❌ Errors:   {count_errors}")
    print(f"📝 Total:    {count_created + count_existed + count_errors}")
    print("=" * 60)


def create_sample_csv():
    """Create sample CSV templates"""
    
    # Sample blogs CSV
    blogs_csv = """title,slug,category,excerpt,content,tags,is_published,featured,read_time,added_date
"MEP Engineering Services in Dubai","mep-engineering-dubai","Engineering","Comprehensive MEP engineering solutions for your projects in Dubai and UAE.","<h2>Introduction to MEP Engineering</h2><p>MEP (Mechanical, Electrical, and Plumbing) engineering is crucial for modern construction projects. Our team provides comprehensive solutions tailored to your needs.</p><h3>Our Services</h3><ul><li>HVAC Design</li><li>Electrical Systems</li><li>Plumbing Solutions</li><li>Fire Protection</li></ul>","mep,engineering,dubai,hvac",true,true,8,"2025-10-01 10:00:00"
"BIM Technology in Construction","bim-construction-tech","Technology","Building Information Modeling (BIM) revolutionizes construction project management.","<h2>What is BIM?</h2><p>Building Information Modeling (BIM) is a digital representation of physical and functional characteristics of a facility.</p><h3>Benefits of BIM</h3><ul><li>Improved Collaboration</li><li>Cost Reduction</li><li>Better Visualization</li><li>Clash Detection</li></ul>","bim,technology,construction,3d",true,false,6,"2025-10-02 14:30:00"
"Sustainable Architecture Trends 2025","sustainable-architecture-2025","Architecture","Discover the latest trends in sustainable and eco-friendly architecture.","<h2>Green Building in 2025</h2><p>Sustainability is no longer optional—it's essential for modern architecture.</p><h3>Key Trends</h3><ol><li>Net-zero energy buildings</li><li>Renewable materials</li><li>Smart building systems</li><li>Water conservation</li></ol>","sustainability,green,architecture,trends",true,true,10,"2025-10-03 09:00:00"
"""
    
    # Sample news CSV
    news_csv = """title,slug,news_type,frequency,excerpt,content,added_date
"New Project Awarded in Abu Dhabi","new-project-abu-dhabi","project","daily","Das and Partners awarded major infrastructure project in Abu Dhabi.","<p>We are thrilled to announce that Das and Partners has been awarded a prestigious infrastructure project in Abu Dhabi. This AED 150 million project will showcase our expertise in engineering excellence.</p><p>The project includes comprehensive MEP design, structural engineering, and project management services for a mixed-use development.</p>","2025-10-01 09:00:00"
"Weekly Project Updates - October Week 1","weekly-updates-oct-week1","general","weekly","Summary of major project milestones achieved this week.","<h2>This Week's Highlights</h2><ul><li>Phase 1 of Al Ain project completed ahead of schedule</li><li>New team members joined our BIM department</li><li>Client appreciation event held successfully</li><li>3 new project proposals submitted</li></ul><p>Looking forward to another productive week ahead!</p>","2025-10-07 17:00:00"
"Monthly Performance Report - September 2025","monthly-report-sep-2025","general","monthly","Das and Partners September 2025 monthly performance overview.","<h2>September 2025 Overview</h2><h3>Projects Completed</h3><ul><li>Villa Design Project - Dubai</li><li>MEP Retrofit - Sharjah Mall</li><li>Structural Assessment - Abu Dhabi Tower</li></ul><h3>Key Metrics</h3><ul><li>15 Active Projects</li><li>98% Client Satisfaction</li><li>Zero Safety Incidents</li><li>250+ Drawings Delivered</li></ul>","2025-10-01 08:00:00"
"""
    
    # Write sample files
    with open('blogs_sample.csv', 'w', encoding='utf-8') as f:
        f.write(blogs_csv)
    print("✅ Created: blogs_sample.csv")
    
    with open('news_sample.csv', 'w', encoding='utf-8') as f:
        f.write(news_csv)
    print("✅ Created: news_sample.csv")
    
    print("\n📝 Sample CSV files created!")
    print("   - blogs_sample.csv")
    print("   - news_sample.csv")
    print("\n💡 Edit these files with your content, then import:")
    print("   python3 import_content.py blogs blogs_sample.csv")
    print("   python3 import_content.py news news_sample.csv")


def show_usage():
    """Show usage instructions"""
    print("\n" + "=" * 60)
    print("📦 BULK CONTENT IMPORT TOOL")
    print("=" * 60)
    print("\nUsage:")
    print("  python3 import_content.py [command] [file]")
    print("\nCommands:")
    print("  blogs <csv_file>    Import blogs from CSV file")
    print("  news <csv_file>     Import news from CSV file")
    print("  sample              Create sample CSV templates")
    print("  help                Show this help message")
    print("\nExamples:")
    print("  python3 import_content.py blogs my_blogs.csv")
    print("  python3 import_content.py news my_news.csv")
    print("  python3 import_content.py sample")
    print("\n" + "=" * 60)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'help':
        show_usage()
    elif command == 'sample':
        create_sample_csv()
    elif command == 'blogs':
        if len(sys.argv) < 3:
            print("❌ Error: Please provide CSV file path")
            print("Usage: python3 import_content.py blogs <csv_file>")
            sys.exit(1)
        import_blogs(sys.argv[2])
    elif command == 'news':
        if len(sys.argv) < 3:
            print("❌ Error: Please provide CSV file path")
            print("Usage: python3 import_content.py news <csv_file>")
            sys.exit(1)
        import_news(sys.argv[2])
    else:
        print(f"❌ Error: Unknown command '{command}'")
        show_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()





