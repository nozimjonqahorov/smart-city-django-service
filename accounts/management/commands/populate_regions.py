from django.core.management.base import BaseCommand
from config.choices import REGION_CHOICES
from accounts.models import Viloyat, Tuman


class Command(BaseCommand):
    help = 'Populate Viloyat and Tuman data'

    def handle(self, *args, **options):
        viloyatlar = {}
        for region_key, region_label in REGION_CHOICES:
            viloyat, created = Viloyat.objects.get_or_create(name=region_label)
            viloyatlar[region_key] = viloyat
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {viloyat.name}'))

        tumanlar_data = {
            'toshkent_shahar': [
                'Bektemir tumani',
                'Chilonzor tumani',
                'Mirzo Ulug\'bek tumani',
                'Olmazor tumani',
                'Sergeli tumani',
                'Uchtepa tumani',
                'Yakkasaroy tumani',
                'Yunusobod tumani',
            ],
            'toshkent_viloyati': [
                'Nurafshon shahri',
                'Ohangaron tumani',
                'Yangiyo\'l shahri',
                'Zangiota tumani',
            ],
            'andijon': [
                'Andijon shahri',
                'Asaka tumani',
                'Baliqchi tumani',
            ],
            'buxoro': [
                'Buxoro shahri',
                'G\'ijduvon tumani',
                'Qorako\'l tumani',
            ],
            'fargona': [
                'Farg\'ona shahri',
                'Qo\'qon shahri',
                'Marg\'ilon shahri',
            ],
            'jizzax': [
                'Jizzax shahri',
                'Zarbdor tumani',
            ],
            'namangan': [
                'Namangan shahri',
                'Chust tumani',
                'Mingbuloq tumani',
            ],
            'navoiy': [
                'Navoiy shahri',
                'Konimex tumani',
            ],
            'qashqadaryo': [
                'Qarshi shahri',
                'Shahrisabz shahri',
                'Koson tumani',
            ],
            'qoraqalpogiston': [
                'Nukus shahri',
                'To\'rtko\'l tumani',
            ],
            'samarqand': [
                'Samarqand shahri',
                'Kattaqo\'rg\'on shahri',
                'Bulung\'ur tumani',
            ],
            'sirdaryo': [
                'Guliston shahri',
                'Sirdaryo tumani',
            ],
            'surxondaryo': [
                'Termiz shahri',
                'Sherobod tumani',
                'Boysun tumani',
            ],
            'xorazm': [
                'Xiva shahri',
                'Urganch shahri',
                'Xonqa tumani',
            ],
        }

        for region_key, tumanlar in tumanlar_data.items():
            viloyat = viloyatlar.get(region_key)
            if not viloyat:
                continue

            for tuman_name in tumanlar:
                tuman, created = Tuman.objects.get_or_create(viloyat=viloyat, name=tuman_name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created: {tuman.name} ({viloyat.name})'))

        self.stdout.write(self.style.SUCCESS('Successfully populated Viloyat and Tuman data'))
