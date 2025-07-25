from django.shortcuts import render, get_object_or_404
from .models import (
    Facilities, Introduction, Program, MissionVision,
    Testimonial, TeamMember, Contact, Application,
    FAQ, Resource, BlogPost, ProcessStep,
    Requirement, Footer, Video, ContactMessage, NextAdmission, GlobalLearner,SocialMediaLink,TermsAndConditions
)
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .forms import ApplicationForm, ContactForm
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
#from .models import Program#
from datetime import datetime



def home(request):
    # Fetch data for the homepage with limited items per section
    intro = Introduction.objects.first()
    mission_vision = MissionVision.objects.first()
    contact = Contact.objects.first()

    # Paginate sections (3 items per section on homepage)
    programs = Program.objects.all()[:3] 
    admission_requirements = Requirement.objects.all()[:3]
    testimonials = Testimonial.objects.all()[:3]
    team = TeamMember.objects.all()[:4]
    facilities = Resource.objects.filter(category='Facility')[:3]
    faqs = FAQ.objects.all()[:3]
    videos = Video.objects.all().order_by('-created_at')[:3]
    next_admission = NextAdmission.objects.all()[:3]
    social_links = SocialMediaLink.objects.filter(is_active=True)

    current_time = timezone.now().strftime('%I:%M %p WAT on %B %d, %Y')

    return render(request, 'home.html', {
        'intro': intro,
        'programs': programs,
        'admission_requirements': admission_requirements,
        'mission_vision': mission_vision,
        'testimonials': testimonials,
        'team': team,
        'contact': contact,
        'faqs': faqs,
        'facilities': facilities,
        'videos': videos,
        'current_time': current_time,
        'next_admission': next_admission,
        'social_links': social_links
    })

def contact(request):
    contact_info = Contact.objects.first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    # Fetch social media links from Contact model's social_link ManyToManyField
    social_links = contact_info.social_link.filter(is_active=True) if contact_info and hasattr(contact_info, 'social_link') else []
    
    return render(request, 'contact.html', {
        'contact': contact_info,
        'form': form,
        'social_links': social_links,
    })



def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    return render(request, 'contact_form.html', {
        'form': form,
    })



def apply(request):
    programs = Program.objects.all()

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user if request.user.is_authenticated else None
            application.save()

            # Inside your apply view after saving the application
            context = {
                'application': application,
                'year': datetime.now().year
            }
            # Admin email
            try:
                subject_admin = 'New Application Submitted'
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = [settings.ADMIN_EMAIL]

                text_content_admin = render_to_string('emails/application_admin.txt', context)
                html_content_admin = render_to_string('emails/application_admin.html', context)

                msg_admin = EmailMultiAlternatives(subject_admin, text_content_admin, from_email, to_email)
                msg_admin.attach_alternative(html_content_admin, "text/html")
                msg_admin.send()
            except Exception as e:
                print(f'Admin email sending failed: {str(e)}')
                messages.warning(request, 'Application submitted, but failed to notify admin.')

            # Applicant email
            try:
                subject_applicant = f'Application Confirmation - {application.program_applied.title}'
                to_applicant = [application.email]

                text_content_applicant = render_to_string('emails/application_applicant.txt', context)
                html_content_applicant = render_to_string('emails/application_applicant.html', context)

                msg_applicant = EmailMultiAlternatives(subject_applicant, text_content_applicant, from_email, to_applicant)
                msg_applicant.attach_alternative(html_content_applicant, "text/html")
                msg_applicant.send()
                messages.success(request, 'Application submitted successfully! Confirmation email sent.')
            except Exception as e:
                print(f'Applicant email sending failed: {str(e)}')
                messages.warning(request, 'Application submitted, but failed to send confirmation email.')

            return redirect('apply')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = ApplicationForm()

    return render(request, 'apply.html', {'programs': programs, 'form': form})


def search(request):
    query = request.GET.get('q', '')
    programs = Program.objects.filter(title__icontains=query) if query else Program.objects.none()
    faqs = FAQ.objects.filter(question__icontains=query) if query else FAQ.objects.none()
    return render(request, 'search.html', {'programs': programs, 'faqs': faqs, 'query': query})

def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})

def programs(request):
    programs = Program.objects.all()
    for program in programs:
        if program.curriculum:
            program.curriculum_list = program.curriculum.splitlines()
        else:
            program.curriculum_list = ['No curriculum details available']
    return render(request, 'programs.html', {'programs': programs})

def program_detail(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    if program.curriculum:
        program.curriculum_list = program.curriculum.splitlines()
    else:
        program.curriculum_list = ['No curriculum details available']
    return render(request, 'program_detail.html', {'program': program})

def team(request):
    team = TeamMember.objects.all()
    return render(request, 'team.html', {'team': team})



def testimonials(request):
    testimonials = Testimonial.objects.all().order_by('-created_at')
    videos = Video.objects.all().order_by('-created_at')
    context = {
        'testimonials': testimonials,
        'videos': videos,
        'current_time': timezone.localtime(timezone.now()).strftime("%I:%M %p WAT on %A, %B %d, %Y")  # 05:07 PM WAT on Thursday, June 26, 2025
    }
    return render(request, 'testimonials.html', context)


def mission_vision(request):
    mission_vision = MissionVision.objects.first()

    mission_items = []
    if mission_vision and mission_vision.mission:
        lines = mission_vision.mission.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                mission_items.append(line[2:].strip())
    context = {
        'mission_vision': mission_vision,
        'mission_items' : mission_items,
    }
    return render(request, 'mission_vision.html', context)


def contact_info(request):
    contact = Contact.objects.first()
    return render(request, 'contact_info.html', {'contact': contact})

def introduction(request):
    intro = Introduction.objects.first()
    return render(request, 'introduction.html', {'intro': intro})

@login_required
def applications(request):
    user_applications = Application.objects.filter(user=request.user)
    return render(request, 'applications.html', {'applications': user_applications})

def blog(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'blog.html', {'blog_posts': blog_posts})

def blog_detail(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    return render(request, 'blog_detail.html', {'post': post})

def resources(request):
    resources = Resource.objects.filter(is_active=True).order_by('-is_featured', '-date_added')
    categories = Resource.CATEGORY_CHOICES
    return render(request, 'resources.html', {'resources': resources, 'categories':categories})

def resource_detail(request, pk):
    resource =get_object_or_404(Resource, pk=pk, is_active=True)
    return render(request, 'resource_detail.html', {'resource': resource})

def application_process(request):
    steps = ProcessStep.objects.all()
    return render(request, 'application_process.html', {'steps': steps})

def admission_requirements(request):
    requirements = Requirement.objects.all()
    return render(request, 'admission_requirements.html', {'requirements': requirements})

def footer(request):
    footer_content = Footer.objects.first()
    return render(request, 'footer.html', {'footer': footer_content})

def facilities(request):
    facilities = Facilities.objects.all().order_by('-created_at')
    context = {
        'facilities': facilities,
        'total_facilities': facilities.count()
    }
    return render(request, 'facilities.html', context)



def next_admission(request):
    admissions = NextAdmission.objects.filter(is_active=True).order_by('-start_date')
    return render(request, 'next_admission.html', {'admissions': admissions})

def global_learners(request):
    learners = GlobalLearner.objects.filter(is_active=True).order_by('display_order')
    return render(request, 'global_learners.html', {'learners': learners})

def videos(request):
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'videos.html', {'videos': videos})

def terms_conditions(request):
    terms = TermsAndConditions.objects.filter(is_active=True).first()
    return render(request, 'terms_and_conditions.html', {'terms': terms})