from django import forms
from .models import Incident

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['category', 'title', 'description', 'photo', 'address']
        labels = {
            'category': 'Kategoriya',
            'title': 'Sarlavha',
            'description': 'Tavsif',
            'photo': 'Asosiy rasm',
            'address': 'Manzil',
        }
