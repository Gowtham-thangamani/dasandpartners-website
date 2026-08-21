from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from das_app.models import News

class Command(BaseCommand):
    help = 'List weekly news from the last 4 weeks for monthly consolidation'

    def handle(self, *args, **kwargs):
        # Get date 4 weeks ago
        four_weeks_ago = timezone.now() - timedelta(weeks=4)
        
        # Fetch weekly news from last 4 weeks
        weekly_news = News.objects.filter(
            frequency='weekly',
            added_date__gte=four_weeks_ago,
            added_date__lte=timezone.now()
        ).order_by('-added_date')
        
        if not weekly_news:
            self.stdout.write(self.style.WARNING('No weekly news found in the last 4 weeks.'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'\n📊 Weekly News from Last 4 Weeks ({four_weeks_ago.strftime("%b %d, %Y")} - {timezone.now().strftime("%b %d, %Y")})\n'))
        self.stdout.write('=' * 80)
        
        for idx, news in enumerate(weekly_news, 1):
            self.stdout.write(f'\n{idx}. {news.title}')
            self.stdout.write(f'   📅 Date: {news.added_date.strftime("%B %d, %Y")}')
            self.stdout.write(f'   📝 Type: {news.get_news_type_display()}')
            if news.excerpt:
                self.stdout.write(f'   📄 Excerpt: {news.excerpt[:100]}...')
            self.stdout.write('')
        
        self.stdout.write('=' * 80)
        self.stdout.write(self.style.SUCCESS(f'\n✅ Total: {weekly_news.count()} weekly news items ready for monthly consolidation\n'))
        self.stdout.write(self.style.WARNING('\n💡 Tip: Use this information to create a monthly report!'))
        self.stdout.write(self.style.WARNING('   Go to: /add-news/ and select "Monthly Reports" frequency\n'))





