# Smart City Django Service

## Qilingan o'zgarishlar

Ushbu branchda ro'yxatdan o'tish va incident yaratish jarayoniga tuman bo'yicha bog'lanish qo'shildi.

### Viloyat va tuman kiritish

- `config/choices.py` faylida O'zbekiston viloyatlari uchun umumiy `REGION_CHOICES` ro'yxati yaratildi.
- `accounts.User` modeliga `region` choice field qo'shildi.
- `accounts.User` modeliga `city` field qo'shildi.
- `incidents.Incident` modeliga `region` choice field qo'shildi.
- `incidents.Incident` modeliga `city` field qo'shildi.
- Fuqaro ro'yxatdan o'tayotganda `region` ni tanlaydi, `city` ya'ni tuman nomini o'zi yozadi.
- Fuqaro incident yaratganda incidentning `region` va `city` qiymatlari avtomatik ravishda foydalanuvchi profilidan olinadi.
- Operatorning `region` qiymati bor bo'lsa, dashboardda faqat o'z viloyatidagi incidentlar ko'rinadi.
- Yangi incident haqida notification faqat shu viloyatdagi operatorlarga yuboriladi.

### Telefon, ism va familiya

- Ro'yxatdan o'tish formasida `first_name`, `last_name`, `phone`, `region` va `city` maydonlari ishlatiladi.
- `phone` yangi ro'yxatdan o'tishda majburiy qilindi.
- Profil sahifasida foydalanuvchi tumanini yangilashi mumkin.

### Email tasdiqlash

- Oddiy ro'yxatdan o'tishda `email` majburiy qilindi.
- Yangi foydalanuvchi emailni tasdiqlamaguncha `is_active=False` holatda saqlanadi.
- Tasdiqlash havolasi emailga yuboriladi.
- Local developmentda email `console.EmailBackend` orqali terminalda ko'rinadi.
- Email tasdiqlangandan keyin foydalanuvchi avtomatik login bo'ladi va dashboardga o'tadi.

### Google, GitHub va Telegram orqali ro'yxatdan o'tish

- `django-allauth` sozlamalari `config/settings.py` ga ulandi.
- Google, GitHub va Telegram providerlari `INSTALLED_APPS` ga qo'shildi.
- `config/urls.py` ichida `allauth.urls` ulandi.
- Ro'yxatdan o'tish sahifasidagi Google, GitHub va Telegram tugmalari haqiqiy provider login URLlariga bog'landi.
- `accounts.User` modeliga kelajakdagi Telegram ulanishi uchun `telegram_id` field qo'shildi.

## Ishga tushirishdan oldin

Yangi migrationlar qo'shilgani uchun bazani yangilash kerak:

```bash
python manage.py migrate
```

Tekshirish:

```bash
python manage.py check
```

## Social loginni to'liq ulash uchun

Google, GitHub va Telegram loginni ishlatish uchun `django-allauth` kerak bo'ladi:

```bash
pip install django-allauth
```

Loyihada `django-allauth` sozlamalari qo'shib qo'yildi. Endi admin panelda social provider kalitlarini kiritish kerak:

1. `python manage.py migrate` qiling.
2. Admin panelga kiring.
3. `Social applications` bo'limidan provider qo'shing.
4. Google uchun `client id` va `secret key` kiriting.
5. GitHub uchun `client id` va `secret key` kiriting.
6. Telegram uchun bot token/login sozlamalarini kiriting.
7. Har bir providerda `Sites` qismiga hozirgi saytni tanlang.

Muhim: social login orqali kirgan foydalanuvchida `phone`, `region` yoki `city` bo'sh bo'lsa, uni profilni yakunlash sahifasiga yuborish kerak. Aks holda incident yaratishda hudud avtomatik to'g'ri bog'lanmaydi.

## Tekshiruv holati

Quyidagi tekshiruv bajarildi:

```bash
python manage.py check
```

Natija: `System check identified no issues`.
