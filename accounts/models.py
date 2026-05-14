from django.contrib.auth.models import AbstractUser
from django.db import models
from config.choices import REGION_CHOICES

class User(AbstractUser):
    ROLE_CHOICES = (
        ('CITIZEN', 'Fuqaro'),
        ('OPERATOR', 'Operator'),
        ('TECHNICIAN', 'Texnik'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CITIZEN')
    phone = models.CharField(max_length=20, blank=True, null=True)
    region = models.CharField(max_length=50, choices=REGION_CHOICES, blank=True)
    city = models.CharField(max_length=100, blank=True)
    telegram_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    category = models.ForeignKey('incidents.Category', on_delete=models.SET_NULL, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def is_busy(self):
        return self.assigned_incidents.filter(status='IN_PROGRESS').exists()
