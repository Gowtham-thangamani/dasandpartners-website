"""Re-create News and Blog posts recovered from the Internet Archive.

Usage:
    python manage.py import_recovered                      # reads recovered_content/recovered.json
    python manage.py import_recovered --path /some/dir     # bundle directory (holds recovered.json + media/)
    python manage.py import_recovered --dry-run

Idempotent: rows are matched by slug and created or updated; nothing is ever deleted.
Media files from <bundle>/media/ are copied into settings.MEDIA_ROOT (existing files are
left alone unless --overwrite-media is given).
"""
import json
import os
import shutil
from datetime import timezone as dt_timezone

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.dateparse import parse_datetime
from django.utils.text import slugify
from django.utils import timezone

from das_app.models import News, Blogs, BlogCategory


class Command(BaseCommand):
    help = "Import News/Blogs recovered from the Wayback Machine (recovered_content/recovered.json)."

    def add_arguments(self, parser):
        parser.add_argument('--path', default=os.path.join(settings.BASE_DIR, 'recovered_content'),
                            help='Bundle directory containing recovered.json and media/')
        parser.add_argument('--dry-run', action='store_true', help='Show what would change, write nothing')
        parser.add_argument('--overwrite-media', action='store_true',
                            help='Overwrite media files that already exist in MEDIA_ROOT')

    def handle(self, *args, **opts):
        bundle = opts['path']
        dry = opts['dry_run']
        json_path = os.path.join(bundle, 'recovered.json')
        if not os.path.exists(json_path):
            raise CommandError('Not found: %s' % json_path)
        with open(json_path, encoding='utf-8') as fh:
            items = json.load(fh)

        copied = self._copy_media(os.path.join(bundle, 'media'), dry, opts['overwrite_media'])
        self.stdout.write('Media files copied: %d (MEDIA_ROOT=%s)' % (copied, settings.MEDIA_ROOT))

        stats = {'news_created': 0, 'news_updated': 0, 'blog_created': 0, 'blog_updated': 0}
        with transaction.atomic():
            for item in items:
                if item.get('model') == 'news':
                    created = self._import_news(item, dry)
                    stats['news_created' if created else 'news_updated'] += 1
                elif item.get('model') == 'blog':
                    created = self._import_blog(item, dry)
                    stats['blog_created' if created else 'blog_updated'] += 1
            if dry:
                transaction.set_rollback(True)
        self.stdout.write(self.style.SUCCESS(
            '%sNews: %d created, %d updated | Blogs: %d created, %d updated' % (
                '[dry-run] ' if dry else '', stats['news_created'], stats['news_updated'],
                stats['blog_created'], stats['blog_updated'])))

    # -- helpers ---------------------------------------------------------
    def _copy_media(self, src_root, dry, overwrite):
        if not os.path.isdir(src_root):
            return 0
        n = 0
        for dirpath, _dirs, files in os.walk(src_root):
            rel = os.path.relpath(dirpath, src_root)
            dest_dir = os.path.normpath(os.path.join(settings.MEDIA_ROOT, rel))
            for f in files:
                dest = os.path.join(dest_dir, f)
                if os.path.exists(dest) and not overwrite:
                    continue
                if not dry:
                    os.makedirs(dest_dir, exist_ok=True)
                    shutil.copy2(os.path.join(dirpath, f), dest)
                n += 1
        return n

    @staticmethod
    def _date(value):
        dt = parse_datetime(value) if value else None
        if dt is None:
            return timezone.now()
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, dt_timezone.utc)
        return dt

    def _import_news(self, it, dry):
        obj = News.objects.filter(slug=it['slug']).first()
        created = obj is None
        if created:
            obj = News(slug=it['slug'])
        obj.title = it['title'][:255]
        obj.news_type = it.get('news_type') or 'general'
        obj.frequency = it.get('frequency') or 'daily'
        obj.excerpt = (it.get('excerpt') or '')[:300]
        obj.content = it.get('content') or ''
        obj.added_date = self._date(it.get('added_date'))
        if it.get('image'):
            obj.image.name = it['image']
        if not dry:
            obj.save()
        self.stdout.write('  %s news  %s' % ('+' if created else '~', it['slug']))
        return created

    def _import_blog(self, it, dry):
        category = None
        if it.get('category'):
            name = it['category'].strip()[:100]
            category = BlogCategory.objects.filter(name__iexact=name).first()
            if category is None:
                category = BlogCategory(name=name, slug=slugify(name)[:50] or 'general')
                if not dry:
                    category.save()
        obj = Blogs.objects.filter(slug=it['slug']).first()
        created = obj is None
        if created:
            obj = Blogs(slug=it['slug'])
        obj.title = it['title'][:255]
        if category is not None and category.pk:
            obj.category = category
        obj.content = it.get('content') or ''
        obj.excerpt = (it.get('excerpt') or '')[:300]
        obj.tags = (it.get('tags') or '')[:255]
        obj.is_published = it.get('is_published', True)
        obj.featured = it.get('featured', False)
        obj.read_time = it.get('read_time') or 5
        obj.added_date = self._date(it.get('added_date'))
        obj.meta_title = (it.get('meta_title') or '')[:60]
        obj.meta_description = (it.get('meta_description') or '')[:160]
        obj.meta_keywords = (it.get('meta_keywords') or '')[:255]
        if it.get('image'):
            obj.image.name = it['image']
        if not dry:
            obj.save()
        self.stdout.write('  %s blog  %s' % ('+' if created else '~', it['slug']))
        return created
