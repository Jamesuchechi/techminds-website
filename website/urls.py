from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('contact/form/', views.contact_form, name='contact_form'),
    path('apply/', views.apply, name='apply'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('search/', views.search, name='search'),
    path('faq/', views.faq, name='faq'),
    path('programs/', views.programs, name='programs'),
    path('programs/<int:program_id>/', views.program_detail, name='program_detail'),
    path('team/', views.team, name='team'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('mission-vision/', views.mission_vision, name='mission_vision'),
    path('introduction/', views.introduction, name='introduction'),
    path('applications/', views.applications, name='applications'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('resources/', views.resources, name='resources'),
    path('resources/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('application/process/', views.application_process, name='application_process'),
    path('admission/requirements/', views.admission_requirements, name='admission_requirements'),
    path('footer/', views.footer, name='footer'),
    path('facilities/', views.facilities, name='facilities'),
    path('next-admission/',views.next_admission, name='next_admission'),
    path('global-learners/', views.global_learners, name='global_learners'),
    path('videos/', views.videos, name='videos'),
    
]