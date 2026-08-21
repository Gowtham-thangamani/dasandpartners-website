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
