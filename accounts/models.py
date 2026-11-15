from django.db import models
from django.contrib.auth.models import User


class CandidateProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='candidate_profile'
    )
    full_name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    skills = models.TextField()
    experience_years = models.PositiveIntegerField(default=0)
    education = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.full_name

class CV(models.Model):
    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name='cvs'
    )
    file = models.FileField(upload_to='cvs/')
    extracted_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CV - {self.candidate.full_name}"

class Company(models.Model):
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='company_profile'
    )
    company_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name

class Job(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class JobRequirement(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='requirements'
    )
    skill_name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.job.title} - {self.skill_name}"

    class Meta:
        verbose_name = "Job Requirement"
        verbose_name_plural = "Job Requirements"
        unique_together = ('job', 'skill_name')

class JobMatch(models.Model):
    class DeliveryStatus(models.TextChoices):
        PENDING = 'pending', 'Në pritje'
        SENT = 'sent', 'Dërguar'
        FAILED = 'failed', 'Dështoi'

    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name='job_matches'
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='matches'
    )
    match_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )
    matched_skills = models.JSONField(default=list, blank=True)
    delivery_status = models.CharField(
        max_length=20,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Job Match"
        verbose_name_plural = "Job Matches"
        constraints = [
            models.UniqueConstraint(
                fields=['candidate', 'job'],
                name='unique_candidate_job_match'
            )
        ]

    def __str__(self):
        return f"{self.candidate.full_name} - {self.job.title}"

class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return self.title