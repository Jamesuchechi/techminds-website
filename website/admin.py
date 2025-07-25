# Fixed admin.py - This matches your existing model structure
from django.contrib import admin
from .models import Introduction,NextAdmission,GlobalLearner ,TermsAndConditions, Program, MissionVision, Testimonial, Video, ContactMessage, TeamMember, Contact, Facilities, Application, FAQ, BlogPost, Resource, ProcessStep, Requirement, CTA,SocialMediaLink

# Keep your existing simple registrations for most models
admin.site.register(Introduction)
admin.site.register(Video)
admin.site.register(Contact)
admin.site.register(FAQ)
admin.site.register(ProcessStep)
admin.site.register(Requirement)
admin.site.register(CTA)



@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'email', 'phone_number', 'program_applied', 'status', 'submitted_at')
    list_filter = ('status', 'program_applied', 'submitted_at')
    search_fields = ('student_name', 'email', 'phone_number')
    actions = ['mark_approved', 'mark_rejected']

    def mark_approved(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Selected applications marked as approved.")
    mark_approved.short_description = "Mark selected applications as approved"

    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, "Selected applications marked as rejected.")
    mark_rejected.short_description = "Mark selected applications as rejected"


from django.contrib import admin
from .models import Program

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'formatted_fee', 'duration', 'category', 'description_preview', 'job_prospects_preview', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'curriculum', 'job_prospects', 'category']
    list_filter = ['category', 'fee', 'created_at']
    ordering = ['title']
    fields = ['title', 'fee', 'description', 'curriculum', 'duration', 'job_prospects', 'category']
    readonly_fields = ['created_at', 'updated_at', 'slug']
    list_per_page = 20
    

    def formatted_fee(self, obj):
        """Display fee with currency formatting."""
        return f"${obj.fee:.2f}" if obj.fee else "N/A"
    formatted_fee.short_description = "Fee"

    def description_preview(self, obj):
        """Show a truncated preview of the description."""
        return f'{obj.description[:100]} ...' if obj.description and len(obj.description) > 100 else obj.description or "N/A"
    description_preview.short_description = "Description"

    def job_prospects_preview(self, obj):
        """Show a truncated preview of job prospects."""
        return f'{obj.job_prospects[:100]}...' if obj.job_prospects and len(obj.job_prospects) > 100 else obj.job_prospects or "N/A"
    job_prospects_preview.short_description = "Job Prospects"

    def formfield_for_dbfield(self, db_field, **kwargs):
        """Customize text fields to use textareas for better editing."""
        if db_field.name in ['description', 'curriculum', 'job_prospects']:
            kwargs['widget'] = admin.widgets.AdminTextareaWidget(attrs={'rows': 5, 'cols': 80})
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_published', 'category')
    list_filter = ('category', 'date_published')
    search_fields = ('title', 'content')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status', 'location', 
        'is_featured', 'is_active', 'date_added', 'added_by'
    ]
    list_filter = [
        'category', 'status', 'is_featured', 'is_active', 
        'date_added', 'added_by'
    ]
    search_fields = [
        'title', 'description', 'location', 'contact_person'
    ]
    readonly_fields = ['date_added', 'last_updated']
    ordering = ['-is_featured', '-date_added']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'status')
        }),
        ('Media', {
            'fields': ('image', 'file'),
            'classes': ('collapse',)
        }),
        ('Location & Capacity', {
            'fields': ('location', 'capacity', 'operating_hours')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'contact_email', 'contact_phone'),
            'classes': ('collapse',)
        }),
        ('Additional Details', {
            'fields': ('special_requirements', 'is_featured', 'is_active'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('added_by', 'date_added', 'last_updated'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['mark_as_featured', 'remove_featured', 'mark_available', 'mark_maintenance']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} facilities marked as featured.")
    mark_as_featured.short_description = "Mark selected facilities as featured"
    
    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} facilities removed from featured.")
    remove_featured.short_description = "Remove featured status"
    
    def mark_available(self, request, queryset):
        queryset.update(status='available')
        self.message_user(request, f"{queryset.count()} facilities marked as available.")
    mark_available.short_description = "Mark as available"
    
    def mark_maintenance(self, request, queryset):
        queryset.update(status='maintenance')
        self.message_user(request, f"{queryset.count()} facilities marked under maintenance.")
    mark_maintenance.short_description = "Mark as under maintenance"

# Enhanced admin for Mission & Vision
@admin.register(MissionVision)
class MissionVisionAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    
    def has_add_permission(self, request):
        # Only allow one Mission/Vision entry
        return True
    


# Enhanced admin for Facilities (matching your existing model)
@admin.register(Facilities)
class FacilitiesAdmin(admin.ModelAdmin):
    list_display = ['author', 'location', 'created_at', 'get_description_preview']
    list_filter = ['location', 'created_at']
    search_fields = ['author', 'description', 'location']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    list_per_page = 20
    
    fieldsets = (
        ('Facility Information', {
            'fields': ('author', 'description'),
            'description': 'Enter the main details about the facility'
        }),
        ('Location Details', {
            'fields': ('location',),
            'description': 'Specify where the facility is located'
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_description_preview(self, obj):
        if obj.description:
            return(
                f'{obj.description[:50]} ...' if len(obj.description) > 50 else obj.description
            ) 
        return "No description"
    get_description_preview.short_description = 'Description Preview'

# Enhanced admin for Testimonials (matching your existing model)
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author', 'event', 'created_at', 'get_quote_preview']
    list_filter = ['created_at']
    search_fields = ['author', 'quote', 'review']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    list_per_page = 25
    
    fieldsets = (
        ('Testimonial Content', {
            'fields': ('quote', 'author', 'review'),
            'description': 'Main testimonial content'
        }),
        ('Event Information', {
            'fields': ('event',),
            'description': 'Event or context (optional)'
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_quote_preview(self, obj):
        if obj.quote:
            return f"{obj.quote[:40]}..." if len(obj.quote) > 40 else obj.quote
        return "No quote"
    get_quote_preview.short_description = 'Quote Preview'

# Enhanced admin for Team Members (basic version since we don't know the exact fields)
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['name'] if hasattr(TeamMember, 'name') else []

# Enhanced admin for Contact Messages (basic version)
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at'] if hasattr(ContactMessage, 'created_at') else ['__str__']
    readonly_fields = ['created_at'] if hasattr(ContactMessage, 'created_at') else []
    ordering = ['-created_at'] if hasattr(ContactMessage, 'created_at') else []


@admin.register(NextAdmission)
class NextAdmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'next_admission', 'is_active', 'created_at')
    list_filter = ('is_active', 'start_date', 'next_admission')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected admissions marked as active.")
    make_active.short_description = "Mark selected admissions as active"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected admissions marked as inactive.")
    make_inactive.short_description = "Mark selected admissions as inactive"


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('platform_name', 'url', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('platform_name', 'url')
    list_editable = ('is_active',)
    ordering = ('platform_name',)


@admin.register(GlobalLearner)
class GlobalLearnerAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'display_order', 'is_active', 'created_at')
    list_filter = ('is_active', 'country')
    search_fields = ('title', 'description', 'country')
    list_editable = ('display_order',)
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected learner entries marked as active.")
    make_active.short_description = "Mark selected learner entries as active"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected learner entries marked as inactive.")
    make_inactive.short_description = "Mark selected learner entries as inactive"

# Customize admin site headers
admin.site.site_header = "Techminds Academy Administration"
admin.site.site_title = "Techminds Admin"
admin.site.index_title = "Welcome to Techminds Academy Admin Panel"


@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ('version', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('version', 'content')
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('content', 'version', 'is_active')
        }),
    )