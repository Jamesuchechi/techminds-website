from django import forms
from .models import Program, Application, ContactMessage
from django.core.validators import RegexValidator

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['student_name', 'email', 'phone_number', 'attestation', 'program_applied','agreement', 'age']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'attestation': forms.TextInput(attrs={'class': 'form-control'}),
            'program_applied': forms.Select(attrs={'class': 'form-control'}),
            'agreement': forms.CheckboxInput(attrs={'required':'required'}),
            'age' : forms.NumberInput(attrs={'class': 'form_control', 'placeholder' : 'Enter You Age', 'min' : 5, 'required' : 'required'}),
        }
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.replace('+', '').replace('-', '').isdigit():
            raise forms.ValidationError("Phone number must contain only digits, +, or -.")
        return phone_number
    
    def clean_agreement(self):
        if agreement := self.cleaned_data.get('agreement'):
            return agreement
        else:
            raise forms.ValidationError("You must agree to the terms to submit the application.")
        
    


class ContactForm(forms.ModelForm):
    # Predefined inquiry categories
    INQUIRY_CHOICES = [
        ('general', 'General Inquiry'),
        ('support', 'Technical Support'),
        ('feedback', 'Feedback & Suggestions'),
        ('partnership', 'Partnership Opportunities'),
        ('complaint', 'Complaint'),
        ('billing', 'Billing & Payment'),
        ('feature_request', 'Feature Request'),
        ('bug_report', 'Bug Report'),
        ('media', 'Media & Press'),
        ('careers', 'Career Opportunities'),
        ('other', 'Other (Please specify)'),
    ]
    
    # Phone number validator
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name',
            'required': True
        }),
        label='Full Name'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'required': True
        }),
        label='Email Address'
    )
    
    phone_number = forms.CharField(
        max_length=15,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1234567890',
            'required': False
        }),
        label='Phone Number',
        required=False
    )
    
    inquiry_type = forms.ChoiceField(
        choices=INQUIRY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'inquiry-type-select',
            'required': True
        }),
        label='What would you like to discuss?'
    )
    
    custom_subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Please specify your inquiry type',
            'id': 'custom-subject-field',
            'style': 'display: none;'
        }),
        label='Custom Subject',
        required=False
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Please provide details about your inquiry...',
            'required': True
        }),
        label='Your Message'
    )
    
    # Optional: Add a checkbox for newsletter subscription
    subscribe_newsletter = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Subscribe to our newsletter for updates',
        required=False
    )
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone_number', 'message']
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        # Add help text for certain fields
        self.fields['message'].help_text = "Please provide as much detail as possible to help us assist you better."
        self.fields['phone_number'].help_text = "Optional - Include if you prefer a phone call response."
    
    def clean(self):
        cleaned_data = super().clean()
        inquiry_type = cleaned_data.get('inquiry_type')
        custom_subject = cleaned_data.get('custom_subject')
        
        # If 'other' is selected, custom_subject is required
        if inquiry_type == 'other' and not custom_subject:
            raise forms.ValidationError(
                "Please specify your inquiry type when selecting 'Other'."
            )
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Set the subject based on inquiry type
        inquiry_type = self.cleaned_data.get('inquiry_type')
        custom_subject = self.cleaned_data.get('custom_subject')
        
        if inquiry_type == 'other' and custom_subject:
            instance.subject = custom_subject
        else:
            # Get the display name for the inquiry type
            subject_mapping = dict(self.INQUIRY_CHOICES)
            instance.subject = subject_mapping.get(inquiry_type, 'General Inquiry')
        
        if commit:
            instance.save()
        
        return instance