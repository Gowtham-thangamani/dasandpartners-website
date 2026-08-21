from django.utils import timezone

from django.shortcuts import redirect, render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from das_app.forms import ContactForm, HomePageForm, NewsForm, BlogForm
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

from .models import Blogs, News, Subscriber
from .expertise_data import EXPERTISE_DATA

# Create your views here.
def home(request):
    if request.method == 'POST':
        # return HttpResponse("Contact Page")
        form = HomePageForm(request.POST)
        # return HttpResponse(form)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            # return HttpResponse("dd")
            subject = f'New Project Form Submission from {name}'
            body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,      # From email
                ['noumannazir99@gmail.com'],      # To email (your receiving address)
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully.")
            form = HomePageForm()
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = HomePageForm()
        
    # Fetch latest blogs and news from database
    latest_blogs = Blogs.objects.filter(added_date__lte=timezone.now()).order_by('-added_date')[:3]
    project_news = News.objects.filter(added_date__lte=timezone.now(), news_type='project').order_by('-added_date')[:3]
    overall_news = News.objects.filter(added_date__lte=timezone.now(), news_type='general').order_by('-added_date')[:3]
    
    context = {
        'form': form,
        'latest_blogs': latest_blogs,
        'project_news': project_news,
        'overall_news': overall_news,
    }
    return render(request, 'index.html', context)


def about(request):
    # Fetch latest blogs and news from database
    latest_blogs = Blogs.objects.filter(added_date__lte=timezone.now()).order_by('-added_date')[:3]
    project_news = News.objects.filter(added_date__lte=timezone.now(), news_type='project').order_by('-added_date')[:3]
    overall_news = News.objects.filter(added_date__lte=timezone.now(), news_type='general').order_by('-added_date')[:3]
    
    context = {
        'latest_blogs': latest_blogs,
        'project_news': project_news,
        'overall_news': overall_news,
    }
    return render(request, 'about.html', context)

def our_expertise(request):
    from .expertise_data import ALL_EXPERTISE_AREAS
    context = {
        'expertise_areas': ALL_EXPERTISE_AREAS
    }
    return render(request, 'our_expertise.html', context)

def our_work(request):
    return render(request, 'our_work.html')

def news(request):
    # Fetch news by type and frequency
    project_news = News.objects.filter(added_date__lte=timezone.now(), news_type='project').order_by('-added_date')
    overall_news = News.objects.filter(added_date__lte=timezone.now(), news_type='general').order_by('-added_date')
    
    # Fetch news by frequency
    daily_news = News.objects.filter(added_date__lte=timezone.now(), frequency='daily').order_by('-added_date')
    weekly_news = News.objects.filter(added_date__lte=timezone.now(), frequency='weekly').order_by('-added_date')
    monthly_news = News.objects.filter(added_date__lte=timezone.now(), frequency='monthly').order_by('-added_date')
    
    context = {
        'project_news': project_news,
        'overall_news': overall_news,
        'daily_news': daily_news,
        'weekly_news': weekly_news,
        'monthly_news': monthly_news,
    }
    return render(request, 'news.html', context)

def blogs(request):
    blogs = Blogs.objects.filter(added_date__lte=timezone.now()).order_by('-added_date')
    context = {
        'blogs': blogs        
    }
    return render(request, 'blogs.html', context)

def blog_details(request , slug):
    blog_obj = Blogs.objects.filter(slug=slug).first()
    
    # Increment view count
    if blog_obj:
        blog_obj.view_count += 1
        blog_obj.save(update_fields=['view_count'])
    
    # Get related blogs from same category
    related_blogs = []
    if blog_obj and blog_obj.category:
        related_blogs = Blogs.objects.filter(
            category=blog_obj.category,
            is_published=True
        ).exclude(id=blog_obj.id).order_by('-created_date')[:3]
    
    context = {
        'blog_obj': blog_obj,
        'related_blogs': related_blogs,
    }
    return render(request, 'blog_details.html', context)

def news_details(request, slug):
    news_obj = News.objects.filter(slug=slug).first()
    
    # Get related news of same type
    related_news = []
    if news_obj:
        related_news = News.objects.filter(
            news_type=news_obj.news_type
        ).exclude(id=news_obj.id).order_by('-added_date')[:3]
    
    context = {
        'news_obj': news_obj,
        'related_news': related_news,
    }
    return render(request, 'news_details.html', context)
    
def careers(request):
    
    return render(request, 'careers.html')

def contact(request):

    if request.method == 'POST':
        # return HttpResponse("Contact Page")
        form = ContactForm(request.POST)
        # return HttpResponse(form)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            type = form.cleaned_data['type']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            # return HttpResponse("dd")
            subject = f'New ({type}) Contact Form Submission from {name}'
            body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,      # From email
                ['noumannazir99@gmail.com'],      # To email (your receiving address)
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully.")
            form = ContactForm()
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})



def architectural_engineering(request):
    return render(request, 'architectural_engineering.html')

def architect_of_record(request):
    return render(request, 'architect_of_record.html')

def oil_and_gas_engineering(request):
    return render(request, 'oil_and_gas_engineering.html')

def structural_engineering(request):
    return render(request, 'structural_engineering.html')

def infrastructure(request):
    return render(request, 'infrastructure.html')

def construction_engineering(request):
    return render(request, 'construction_engineering.html')

def mep_engineering(request):
    return render(request, 'mep_engineering.html')

def project_management(request):
    return render(request, 'project_management.html')

def villa_design(request):
    return render(request, 'villa_design.html')

def villa_design_abu_dhabi(request):
    return render(request, 'villa_design_abu_dhabi.html')

def interior_design(request):
    return render(request, 'interior_design.html')

def building_information_modeling(request):
    return render(request, 'building_information_modeling.html')

def lead_consultant(request):
    return render(request, 'lead_consultant.html')

def contract_cost_consultancy(request):
    return render(request, 'contract_cost_consultancy.html')

def facilities_management_consultancy(request):
    return render(request, 'facilities_management_consultancy.html')
    
def renewable_energy_consultants(request):
    return render(request, 'renewable_energy_consultants.html')
def mall_management_consultants(request):
    return render(request, 'mall_management_consultants.html')

def leed_consultants(request):
    return render(request, 'leed_consultants.html')

def electrical_engineering_consultancy(request):
    return render(request, 'electrical_engineering_consultancy.html')

def life_at_dap(request):
    # Gallery items for the Life at DAP page
    gallery_items = [
        {
            'img': 'assets/images/life/1.jpeg',
            'alt': 'Team Collaboration',
            'icon': 'fas fa-users',
            'caption': 'Team Collaboration'
        },
        {
            'img': 'assets/images/life/WhatsApp Image 2025-07-17 at 6.26.12 PM.jpeg',
            'alt': 'Innovation Hub',
            'icon': 'fas fa-lightbulb',
            'caption': 'Innovation Hub'
        },
        {
            'img': 'assets/images/life/WhatsApp Image 2025-07-17 at 6.34.46 PM.jpeg',
            'alt': 'Work Environment',
            'icon': 'fas fa-building',
            'caption': 'Work Environment'
        },
        {
            'img': 'assets/images/life/WhatsApp Image 2025-07-17 at 6.34.47 PM.jpeg',
            'alt': 'Celebrations',
            'icon': 'fas fa-gift',
            'caption': 'Celebrations'
        }
    ]
    
    context = {
        'gallery_items': gallery_items
    }
    return render(request, 'life_at_dap.html', context)

def login(request):    return render(request, 'login.html')

# New Service Views
def csa_services(request):
    return render(request, 'csa_services.html')

def mep_services(request):
    return render(request, 'mep_services.html')

def eit_services(request):
    return render(request, 'eit_services.html')

def hsse_services(request):
    return render(request, 'hsse_services.html')

def bim_services(request):
    return render(request, 'bim_services.html')

def contract_administration(request):
    return render(request, 'contract_administration.html')

def unified_expertise(request, expertise_key):
    """
    Unified view for all expertise pages using the template and data structure
    """
    if expertise_key in EXPERTISE_DATA:
        expertise_data = EXPERTISE_DATA[expertise_key]
        
        # Prepare context for the template
        context = {
            'expertise_title': expertise_data['title'],
            'expertise_subtitle': expertise_data['subtitle'],
            'expertise_hero_title': expertise_data['hero_title'],
            'expertise_hero_description': expertise_data['hero_description'],
            'expertise_hero_image': expertise_data['hero_image'],
            'expertise_banner_image': expertise_data['banner_image'],
            'expertise_badge_text': expertise_data['badge_text'],
            'expertise_overview_subtitle': expertise_data['overview_subtitle'],
            'expertise_overview_description': expertise_data['overview_description'],
            'expertise_detail_image': expertise_data['detail_image'],
            'expertise_detail_title': expertise_data['detail_title'],
            'expertise_detail_intro': expertise_data['detail_intro'],
            'expertise_services_image': expertise_data['services_image'],
            'expertise_services_description': expertise_data['services_description'],
            'expertise_services_overview': expertise_data['services_overview'],
            'expertise_responsibilities_title': expertise_data['responsibilities_title'],
            'expertise_responsibilities_intro': expertise_data['responsibilities_intro'],
            'expertise_additional_image': expertise_data['additional_image'],
            'expertise_cta_title': expertise_data['cta_title'],
            'expertise_cta_description': expertise_data['cta_description'],
            'expertise_stats': expertise_data['stats'],
            'expertise_services': expertise_data['services'],
            'expertise_responsibilities': expertise_data['responsibilities'],
            'expertise_additional_info_left': expertise_data['additional_info_left'],
            'expertise_additional_info_right': expertise_data['additional_info_right'],
            'expertise_conclusion': expertise_data.get('conclusion', ''),
        }
        
        return render(request, 'expertise_template.html', context)
    else:
        # Handle case where expertise key doesn't exist
        return redirect('our_expertise')

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not Subscriber.objects.filter(email=email).exists():
            Subscriber.objects.create(email=email)
            messages.success(request, "Subscribed successfully!")
        else:
            messages.info(request, "You're already subscribed.")
        return redirect(request.META.get('HTTP_REFERER', 'home'))



def our_people(request):
    return render(request, 'our_people.html')

def gallery(request):
    gallery_data = {
        'fsl': [
            {'src': 'assets/images/football/Unknown-25.jpeg', 'title': 'DAP FSL 1'},
            {'src': 'assets/images/football/Unknown-26.jpeg', 'title': 'DAP FSL 2'},
            {'src': 'assets/images/football/Unknown-28.jpeg', 'title': 'DAP FSL 3'},
            {'src': 'assets/images/football/Unknown-29.jpeg', 'title': 'DAP FSL 4'},
            {'src': 'assets/images/football/Unknown-30.jpeg', 'title': 'DAP FSL 5'},
            {'src': 'assets/images/football/Unknown-31.jpeg', 'title': 'DAP FSL 6'},
            {'src': 'assets/images/football/Unknown-33.jpeg', 'title': 'DAP FSL 7'},
            {'src': 'assets/images/football/Unknown-34.jpeg', 'title': 'DAP FSL 8'},
            {'src': 'assets/images/football/IMG_2933.jpg', 'title': 'DAP FSL 9'},
        ],
        'religious': [
            {'src': 'assets/images/relevents/Unknown-25.jpeg', 'title': 'Cultural Event 1'},
            {'src': 'assets/images/relevents/Unknown-26.jpeg', 'title': 'Cultural Event 2'},
            {'src': 'assets/images/relevents/Unknown-27.jpeg', 'title': 'Cultural Event 3'},
            {'src': 'assets/images/relevents/Unknown-28.jpeg', 'title': 'Cultural Event 4'},
            {'src': 'assets/images/relevents/Unknown-29.jpeg', 'title': 'Cultural Event 5'},
            {'src': 'assets/images/relevents/Unknown-30.jpeg', 'title': 'Cultural Event 6'},
            # {'src': 'assets/images/relevents/Unknown-31.jpeg', 'title': 'Cultural Event 7'},
            {'src': 'assets/images/relevents/Unknown-32.jpeg', 'title': 'Cultural Event 8'},
            {'src': 'assets/images/relevents/WhatsApp Image 2025-09-30 at 11.10.11 AM.jpeg', 'title': 'Cultural Event 9'},
        ],
        'csr': [
            {'src': 'assets/images/csrpic/Unknown-25.jpeg', 'title': 'CSR Event 1'},
            {'src': 'assets/images/csrpic/Unknown-27.jpeg', 'title': 'CSR Event 2'},
            {'src': 'assets/images/csrpic/Unknown-28.jpeg', 'title': 'CSR Event 3'},
            {'src': 'assets/images/csrpic/Unknown-29.jpeg', 'title': 'CSR Event 4'},
            {'src': 'assets/images/csrpic/Unknown-30.jpeg', 'title': 'CSR Event 5'},
            {'src': 'assets/images/csrpic/Unknown-31.jpeg', 'title': 'CSR Event 6'},
            {'src': 'assets/images/csrpic/Unknown-32.jpeg', 'title': 'CSR Event 7'},
            {'src': 'assets/images/csrpic/Unknown-33.jpeg', 'title': 'CSR Event 8'},
            {'src': 'assets/images/csrpic/Unknown-34.jpeg', 'title': 'CSR Event 9'},
        ],
        'annual': [
            # {'src': 'assets/images/annual/WhatsApp Image 2025-07-20 at 3.14.39 PM.jpeg', 'title': 'Annual Dinner 1'},
            {'src': 'assets/images/annual/WhatsApp Image 2025-07-20 at 3.14.39 PM (1).jpeg', 'title': 'Annual Dinner 2'},
            {'src': 'assets/images/annual/WhatsApp Image 2025-07-20 at 3.15.59 PM (1).jpeg', 'title': 'Annual Dinner 3'},
            # {'src': 'assets/images/annual/WhatsApp Image 2025-07-20 at 3.15.59 PM (2).jpeg', 'title': 'Annual Dinner 4'},
            # {'src': 'assets/images/annual/WhatsApp Image 2025-07-20 at 3.16.00 PM.jpeg', 'title': 'Annual Dinner 5'},
            # {'src': 'assets/images/annual/WhatsApp Image 2025-07-20 at 3.17.23 PM (1).jpeg', 'title': 'Annual Dinner 6'},
            # {'src': 'assets/images/annual/WhatsApp Image 2025-07-20 at 3.23.10 PM.jpeg', 'title': 'Annual Dinner 7'},
            {'src': 'assets/images/annual/WhatsApp Image 2025-07-20 at 3.23.32 PM (1).jpeg', 'title': 'Annual Dinner 8'},
            # {'src': 'assets/images/annual/WhatsApp Image 2025-07-20 at 3.14.39 PM (1).jpeg', 'title': 'Annual Dinner 9'},
        ],
    }
    return render(request, 'gallery.html', {'gallery_data': gallery_data})

# Content Management Portal Views
@login_required(login_url='/login/')
def content_dashboard(request):
    """Content Management Dashboard"""
    total_news = News.objects.count()
    total_blogs = Blogs.objects.count()
    recent_news = News.objects.order_by('-created_date')[:5]
    recent_blogs = Blogs.objects.order_by('-created_date')[:5]
    
    context = {
        'total_news': total_news,
        'total_blogs': total_blogs,
        'recent_news': recent_news,
        'recent_blogs': recent_blogs,
    }
    return render(request, 'content_portal/dashboard.html', context)

@login_required(login_url='/login/')
def add_news(request):
    """Add new news article"""
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'News article added successfully!')
            return redirect('content_dashboard')
    else:
        form = NewsForm()
    
    return render(request, 'content_portal/add_news.html', {'form': form})

@login_required(login_url='/login/')
def add_blog(request):
    """Add new blog post"""
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post added successfully!')
            return redirect('content_dashboard')
    else:
        form = BlogForm()
    
    return render(request, 'content_portal/add_blog.html', {'form': form})

@login_required(login_url='/login/')
def news_list(request):
    """List all news articles"""
    news_list = News.objects.order_by('-created_date')
    paginator = Paginator(news_list, 10)  # Show 10 news per page
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    return render(request, 'content_portal/news_list.html', {'news': news})

@login_required(login_url='/login/')
def blog_list(request):
    """List all blog posts"""
    blog_list = Blogs.objects.order_by('-created_date')
    paginator = Paginator(blog_list, 10)  # Show 10 blogs per page
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    
    return render(request, 'content_portal/blog_list.html', {'blogs': blogs})

@login_required(login_url='/login/')
def edit_news(request, news_id):
    """Edit news article"""
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'News article updated successfully!')
            return redirect('news_list')
    else:
        form = NewsForm(instance=news)
    
    return render(request, 'content_portal/edit_news.html', {'form': form, 'news': news})

@login_required(login_url='/login/')
def edit_blog(request, blog_id):
    """Edit blog post"""
    blog = get_object_or_404(Blogs, id=blog_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('blog_list')
    else:
        form = BlogForm(instance=blog)
    
    return render(request, 'content_portal/edit_blog.html', {'form': form, 'blog': blog})

@login_required(login_url='/login/')
def delete_news(request, news_id):
    """Delete news article"""
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'News article deleted successfully!')
        return redirect('news_list')
    
    return render(request, 'content_portal/delete_news.html', {'news': news})

@login_required(login_url='/login/')
def delete_blog(request, blog_id):
    """Delete blog post"""
    blog = get_object_or_404(Blogs, id=blog_id)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('blog_list')
    
    return render(request, 'content_portal/delete_blog.html', {'blog': blog})

# Authentication Views
def login_view(request):
    """Login view for content management"""
    if request.user.is_authenticated:
        return redirect('content_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'content_dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

@login_required(login_url='/login/')
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')
