from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from incidents.models import Category

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label="Ism")
    last_name = forms.CharField(max_length=30, label="Familiya")
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label="Sizning rolingiz")
    phone = forms.CharField(required=False, label="Telefon raqami")
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        required=False, 
        label="Ixtisoslik (faqat Texniklar uchun)",
        help_text="Fuqarolar va Operatorlar uchun shart emas."
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'role', 'phone', 'category', 'avatar')
        labels = {
            'username': 'Foydalanuvchi nomi',
            'email': 'Email manzili',
            'avatar': 'Profil surati',
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'category', 'avatar']
        labels = {
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'email': 'Email manzili',
            'phone': 'Telefon raqami',
            'category': 'Ixtisoslik (Texniklar uchun)',
            'avatar': 'Profil surati',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.role != 'TECHNICIAN':
            self.fields['category'].widget = forms.HiddenInput()
