from django.utils import timezone

from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from das_app.forms import ContactForm, HomePageForm
from django.contrib import messages
from django.http import HttpResponse

from .models import Blogs, News, Subscriber

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
        
    latest_blogs = Blogs.objects.order_by('-created_date')[:2]
    return render(request, 'index.html', {'form': form, 'latest_blogs': latest_blogs})


def about(request):
    return render(request, 'about.html')

def our_expertise(request):
    return render(request, 'our_expertise.html')

def our_work(request):
    return render(request, 'our_work.html')

def news(request):
    news = News.objects.filter(added_date__lte=timezone.now()).order_by('-added_date')
    # return HttpResponse(news)
    context = {
        'news': news        
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
    # return HttpResponse(blog_obj)
    context = {
        'blog_obj': blog_obj        
    }
    return render(request, 'blog_details.html', context)
    
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
    return render(request, 'life_at_dap.html')

def login(request):
    return render(request, 'login.html')


def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not Subscriber.objects.filter(email=email).exists():
            Subscriber.objects.create(email=email)
            messages.success(request, "Subscribed successfully!")
        else:
            messages.info(request, "You're already subscribed.")
        return redirect(request.META.get('HTTP_REFERER', 'home'))


