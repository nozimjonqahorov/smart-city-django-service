from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('CITIZEN', 'Fuqaro'),
        ('OPERATOR', 'Operator'),
        ('TECHNICIAN', 'Texnik'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CITIZEN')
    phone = models.CharField(max_length=20, blank=True, null=True)
    category = models.ForeignKey('incidents.Category', on_delete=models.SET_NULL, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def is_busy(self):
        return self.assigned_incidents.filter(status='IN_PROGRESS').exists()
