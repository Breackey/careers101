from django import forms
from .models import NewsletterUser, Newsletter
from crispy_forms.helper import FormHelper

class NewsletterUserSubscribeForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False
    
    
    class Meta:
        model = NewsletterUser
        fields =['email']

        def clean_email(self):
            email = self.cleaned_data.get('email')

            return email

class NewsletterCreationForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields= ['subject','body','email','status']