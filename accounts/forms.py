from django import forms
from django.contrib.auth.forms import UserCreationForm
from config.choices import REGION_CHOICES
from .models import User, Viloyat, Tuman
from incidents.models import Category

REGION_VALUE_BY_LABEL = {label: value for value, label in REGION_CHOICES}


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email manzili")
    first_name = forms.CharField(max_length=30, label="Ism")
    last_name = forms.CharField(max_length=30, label="Familiya")
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label="Sizning rolingiz")
    phone = forms.CharField(required=True, label="Telefon raqami")
    region = forms.ModelChoiceField(
        queryset=Viloyat.objects.none(),
        empty_label="Viloyatni tanlang",
        label="Viloyat",
    )
    city = forms.ModelChoiceField(
        queryset=Tuman.objects.none(),
        empty_label="Avval viloyatni tanlang",
        label="Tuman",
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        required=False, 
        label="Ixtisoslik (faqat Texniklar uchun)",
        help_text="Fuqarolar va Operatorlar uchun shart emas."
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'role', 'phone', 'region', 'city', 'category', 'avatar')
        labels = {
            'username': 'Foydalanuvchi nomi',
            'email': 'Email manzili',
            'region': 'Viloyat',
            'city': 'Tuman',
            'avatar': 'Profil surati',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['region'].queryset = Viloyat.objects.order_by('name')
        self.fields['city'].queryset = Tuman.objects.none()
        self.fields['city'].widget.attrs['disabled'] = 'disabled'

        region_id = None
        if self.is_bound:
            region_id = self.data.get('region')
        elif self.initial.get('region'):
            region_id = self.initial.get('region')

        if region_id:
            self.fields['city'].queryset = Tuman.objects.filter(viloyat_id=region_id).order_by('name')
            self.fields['city'].widget.attrs.pop('disabled', None)

    def clean_region(self):
        region = self.cleaned_data.get('region')
        if region and region.name not in REGION_VALUE_BY_LABEL:
            raise forms.ValidationError("Tanlangan viloyat tizimdagi viloyatlar ro'yxatiga mos emas.")
        return region

    def clean(self):
        cleaned_data = super().clean()
        region = cleaned_data.get('region')
        city = cleaned_data.get('city')

        if region and city and city.viloyat_id != region.id:
            self.add_error('city', "Tanlangan tuman viloyatga tegishli emas.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        region = self.cleaned_data.get('region')
        city = self.cleaned_data.get('city')

        user.region = REGION_VALUE_BY_LABEL.get(region.name, '') if region else ''
        user.city = city.name if city else ''

        if commit:
            user.save()
            self.save_m2m()

        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'region', 'city', 'category', 'avatar']
        labels = {
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'email': 'Email manzili',
            'phone': 'Telefon raqami',
            'region': 'Viloyat',
            'city': 'Tuman',
            'category': 'Ixtisoslik (Texniklar uchun)',
            'avatar': 'Profil surati',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.role != 'TECHNICIAN':
            self.fields['category'].widget = forms.HiddenInput()
