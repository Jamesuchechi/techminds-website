from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone

# Introduction and Overview
class Introduction(models.Model):
    overview = models.TextField()  # Brief overview of the academy's purpose
    featured_programs = models.TextField()  # Highlight key programs

    def __str__(self):
        return "Introduction"

# Programs/Courses
class Program(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    curriculum = models.TextField()
    duration = models.CharField(max_length=100)
    job_prospects = models.TextField()
    fee = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200,unique=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']

# Mission and Vision
class MissionVision(models.Model):
    mission = models.TextField()
    vision = models.TextField()

    def __str__(self):
        return f"Mission: {self.mission[:30]}... | Vision: {self.vision[:30]}..."
    

class Facilities(models.Model):
    author = models.CharField(max_length=100, help_text='Name of the facility e.g Modern Computer Lab' )
    description = models.TextField(help_text='Detailed description of the Facility')
    location = models.CharField(max_length=200, help_text='Physical location of the facility')
    created_at = models.DateTimeField(auto_now_add=True)
    capacity = models.PositiveIntegerField(null=True,blank=True, help_text='maximum capacity of the facility')
    is_active = models.BooleanField(default=True,help_text='Is this facility currently available')
    image = models.ImageField(upload_to='facilities/', null=True,blank=True,help_text='Upload an image of of the facility ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Facility'
        verbose_name_plural = 'Facilities'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

# Testimonials
class Testimonial(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=100)
    event = models.CharField(max_length=100, blank=True, null=True)  
    review = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}'s Testimonial"
    
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField()  # URL to the video
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Team Members
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(max_length=100)
    image = models.ImageField(upload_to='team_images/', blank=True, null=True)

    def __str__(self):
        return self.name

# Contact Information
class Contact(models.Model):
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    office_hours = models.CharField(max_length=100)
    social_link = models.ManyToManyField('SocialMediaLink',blank=True)

    def __str__(self):
        return self.email
    
class ContactMessage(models.Model):
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
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=100, choices=INQUIRY_CHOICES, default='general')
    message = models.TextField()
    subscribe_newsletter = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    student_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    attestation = models.TextField(max_length= 1000, blank=True, null=True)
    age = models.IntegerField()
    agreement = models.BooleanField(default=False)
    program_applied = models.ForeignKey(Program, on_delete=models.CASCADE)
    submitted_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending",choices=[('approved', 'Approved'),('pending', 'Pending'),('rejected','Rejected')])

    def __str__(self):
        return f"{self.student_name} - {self.program_applied.title}"

# FAQs
class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question
    

# Blog Post
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

# Resource (Library)


class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('laboratory', 'Laboratory'),
        ('library', 'Library'),
        ('classroom', 'Classroom'),
        ('technology', 'Technology'),
        ('maker_space', 'Maker Space'),
        ('computer_lab', 'Computer Lab'),
        ('research_center', 'Research Center'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('maintenance', 'Under Maintenance'),
        ('unavailable', 'Unavailable'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='other')
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    image = models.ImageField(upload_to='resources/images/', blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    capacity = models.IntegerField(blank=True, null=True, help_text="Maximum capacity if applicable")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    contact_person = models.CharField(max_length=200, blank=True, help_text="Person in charge")
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    operating_hours = models.CharField(max_length=200, blank=True, help_text="e.g., 8:00 AM - 6:00 PM")
    special_requirements = models.TextField(blank=True, help_text="Any special requirements or rules")
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_resources')
    is_featured = models.BooleanField(default=False, help_text="Display prominently on facilities page")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-is_featured', '-date_added']
        verbose_name = "School Resource/Facility"
        verbose_name_plural = "School Resources/Facilities"
    
    def _str_(self):
        return self.title

# Call to Action
class CTA(models.Model):
    text = models.CharField(max_length=200)
    link = models.URLField()
    placement = models.CharField(max_length=50)  # e.g., 'header', 'footer'

    def __str__(self):
        return self.text

# Application Process Step
class ProcessStep(models.Model):
    step_number = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"Step {self.step_number}"

# Admissions Requirement
class Requirement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

# Footer (extend Contact or create new)
class Footer(models.Model):
    copyright = models.TextField()
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "Footer Content"
    
class NextAdmission(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    next_admission = models.DateField()
    description = models.TextField()
    banner_image = models.ImageField(upload_to='admissions/banners/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class GlobalLearner(models.Model):
    title = models.CharField(max_length=200)  # e.g., "Learners Worldwide" or testimonial name
    description = models.TextField()  # e.g., stats like "10,000 learners" or testimonial text
    image = models.ImageField(upload_to='learners/images/', null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)  # Optional for testimonials or stats
    display_order = models.PositiveIntegerField(default=0)  # For sorting
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['display_order']


class SocialMediaLink(models.Model):
    platform_name = models.CharField(max_length=50, unique=True)
    url = models.URLField(max_length=200)
    icon_class = models.CharField(max_length=100, blank=True, help_text="Font Awesome class for icon (e.g., 'fab fa-twitter')")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Social Media Link"
        verbose_name_plural = "Social Media Links"
        ordering = ['platform_name']

    def __str__(self):
        return self.platform_name
    
class TermsAndConditions(models.Model):
    content = models.TextField()
    version = models.CharField(max_length=10, unique=True,blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Terms and Condition"
        verbose_name_plural = "Terms and Conditions"
        ordering = ['-created_at']

    def __str__(self):
        return f"Terms v{self.version} ({'Active' if self.is_active else 'Inactive'})"