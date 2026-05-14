from django.contrib.auth.models import AbstractUser
from django.db import models
from config.choices import REGION_CHOICES


class Viloyat(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyatlar"
        ordering = ['name']

    def __str__(self):
        return self.name


class Tuman(models.Model):
    name = models.CharField(max_length=100)
    viloyat = models.ForeignKey(Viloyat, on_delete=models.CASCADE, related_name='tumans')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tuman"
        verbose_name_plural = "Tumanlar"
        ordering = ['viloyat', 'name']
        unique_together = ('viloyat', 'name')

    def __str__(self):
        return f"{self.name} ({self.viloyat.name})"


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
