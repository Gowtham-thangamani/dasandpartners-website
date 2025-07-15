from django import forms
from captcha.fields import CaptchaField

SUBJECT_CHOICES = [
    ('', 'Select Type'),        # Placeholder/default
    ('project', 'New Project'),
    ('message', 'Message'),
    ('careers', 'Careers'),
]

class HomePageForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control style', 'placeholder': 'Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control style', 'placeholder': 'Email'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control style', 'placeholder': 'Subject'})
        self.fields['message'].widget.attrs.update({'class': 'form-control style', 'placeholder': 'Message'})
        self.fields['captcha'].widget.attrs.update({'class': 'form-control style'})


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    type = forms.ChoiceField(choices=SUBJECT_CHOICES, required=True)
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control style', 'placeholder': 'Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control style', 'placeholder': 'Email'})
        self.fields['type'].widget.attrs.update({'class': 'form-select style', 'placeholder': 'Type'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control style', 'placeholder': 'Subject'})
        self.fields['message'].widget.attrs.update({'class': 'form-control style', 'placeholder': 'Message'})
        self.fields['captcha'].widget.attrs.update({'class': 'form-control style'})

