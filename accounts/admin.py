from django.contrib import admin
from .models import CandidateProfile, Company, CV, Job, JobRequirement, JobMatch, Notification


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'profession', 'experience_years')
    search_fields = ('full_name', 'profession')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'location')
    search_fields = ('company_name', 'location')

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'uploaded_at')
    search_fields = ('candidate__full_name',)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'employment_type', 'is_active')
    search_fields = ('title', 'company__company_name', 'location')
    list_filter = ('is_active', 'employment_type')

@admin.register(JobRequirement)
class JobRequirementAdmin(admin.ModelAdmin):
    list_display = ('job', 'skill_name')
    search_fields = ('job__title', 'skill_name')
    list_filter = ('job',)

@admin.register(JobMatch)
class JobMatchAdmin(admin.ModelAdmin):
    list_display = (
        'candidate',
        'job',
        'match_percentage',
        'delivery_status',
        'created_at'
    )
    search_fields = ('candidate__full_name', 'job__title')
    list_filter = ('delivery_status',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username')
    list_filter = ('is_read', 'created_at')