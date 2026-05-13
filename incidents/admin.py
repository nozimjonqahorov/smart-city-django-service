from django.contrib import admin
from .models import Category, Incident, Feedback, SystemLog

# Register your models here.
admin.site.register(Category)
admin.site.register(Incident)
admin.site.register(Feedback)
admin.site.register(SystemLog)
