from django.db import models
from django.conf import settings
from config.choices import REGION_CHOICES

class Category(models.Model):
    name = models.CharField(max_length=100)
    sla_hours = models.IntegerField(default=24)

    def __str__(self):
        return self.name

class Incident(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'Yangi'),
        ('IN_PROGRESS', 'Jarayonda'),
        ('RESOLVED', 'Bajarildi'),
        ('CLOSED', 'Yopildi'),
        ('REJECTED', 'Rad etildi'),
        ('REOPENED', 'Qayta ochildi'),
    )
    PRIORITY_CHOICES = (
        ('LOW', 'Past'),
        ('MEDIUM', 'O\'rta'),
        ('HIGH', 'Yuqori'),
    )

    citizen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reported_incidents')
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_incidents')
    technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_incidents')
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='incidents/')
    address = models.CharField(max_length=255)
    region = models.CharField(max_length=50, choices=REGION_CHOICES, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    result_photo = models.ImageField(upload_to='results/', blank=True, null=True)
    result_comment = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'category']),
            models.Index(fields=['region']),
            models.Index(fields=['city']),
        ]

    def __str__(self):
        return self.title

class Feedback(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)

class SystemLog(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='logs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class IncidentImage(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='incidents/')

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
