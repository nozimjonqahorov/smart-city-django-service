import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# Wait, my project name is 'config', not 'core'
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from incidents.models import Category

Category.objects.all().delete()
categories = [
    'Elektr tarmoqlari', 
    'Suv ta\'minoti', 
    'Gaz ta\'minoti', 
    'Yo\'l infratuzilmasi', 
    'Ekologiya va tozalik', 
    'Obodonlashtirish', 
    'Kanalizatsiya'
]

for cat in categories:
    Category.objects.create(name=cat)
    print(f"Kategoriya yaratildi: {cat}")
