from django import forms
from .models import News, Blogs

# Existing forms for contact and homepage
class ContactForm(forms.Form):
    CONTACT_TYPE_CHOICES = [
        ('General Inquiry', 'General Inquiry'),
        ('Project Consultation', 'Project Consultation'),
        ('Career Inquiry', 'Career Inquiry'),
        ('Partnership', 'Partnership'),
        ('Other', 'Other'),
    ]
    
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    type = forms.ChoiceField(choices=CONTACT_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'}))

class HomePageForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'}))


# Project enquiry — forwarded to the dasandpartnersengineering.com admin panel.
class ProjectEnquiryForm(forms.Form):
    PROJECT_TYPE_CHOICES = [
        ('', 'Project Type'),
        ('Architectural / Building', 'Architectural / Building'),
        ('Structural Engineering', 'Structural Engineering'),
        ('MEP Engineering', 'MEP Engineering'),
        ('Infrastructure', 'Infrastructure'),
        ('Oil & Gas / Industrial', 'Oil & Gas / Industrial'),
        ('Authority Approval / NOC', 'Authority Approval / NOC'),
        ('BIM Services', 'BIM Services'),
        ('Other', 'Other'),
    ]
    EMIRATE_CHOICES = [
        ('', 'Emirate'),
        ('Abu Dhabi', 'Abu Dhabi'), ('Dubai', 'Dubai'), ('Sharjah', 'Sharjah'),
        ('Ajman', 'Ajman'), ('Ras Al Khaimah', 'Ras Al Khaimah'),
        ('Fujairah', 'Fujairah'), ('Umm Al Quwain', 'Umm Al Quwain'), ('Other', 'Other'),
    ]
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    phone = forms.CharField(max_length=40, required=False)
    company = forms.CharField(max_length=120, required=False)
    project_type = forms.ChoiceField(choices=PROJECT_TYPE_CHOICES, required=False)
    emirate = forms.ChoiceField(choices=EMIRATE_CHOICES, required=False)
    message = forms.CharField(widget=forms.Textarea, required=False)


# Job application — forwarded (with resume) to the engineering admin panel.
class JobApplicationForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    phone = forms.CharField(max_length=40, required=False)
    job = forms.CharField(max_length=160)
    location = forms.CharField(max_length=80, required=False)
    current_salary = forms.CharField(max_length=40, required=False)
    expected_salary = forms.CharField(max_length=40, required=False)
    cover = forms.CharField(widget=forms.Textarea, required=False)
    cv = forms.FileField(required=False)

# Content Portal Forms
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'slug', 'news_type', 'frequency', 'image', 'excerpt', 'content', 'added_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter news title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'url-friendly-slug (leave blank to auto-generate)'
            }),
            'news_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'frequency': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description (max 300 characters)'
            }),
            'added_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Select publication date and time'
            })
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ['title', 'slug', 'category', 'image', 'excerpt', 'content', 'tags', 'is_published', 'featured', 'read_time', 'added_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter blog title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'url-friendly-slug (leave blank to auto-generate)'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description (max 300 characters)'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'tag1, tag2, tag3'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'read_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Estimated reading time in minutes'
            }),
            'added_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Select publication date and time'
            })
        }
