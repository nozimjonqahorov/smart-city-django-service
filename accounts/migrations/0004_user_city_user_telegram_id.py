from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_user_avatar_alter_user_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="region",
            field=models.CharField(
                blank=True,
                choices=[
                    ("andijon", "Andijon viloyati"),
                    ("buxoro", "Buxoro viloyati"),
                    ("fargona", "Farg'ona viloyati"),
                    ("jizzax", "Jizzax viloyati"),
                    ("namangan", "Namangan viloyati"),
                    ("navoiy", "Navoiy viloyati"),
                    ("qashqadaryo", "Qashqadaryo viloyati"),
                    ("qoraqalpogiston", "Qoraqalpog'iston Respublikasi"),
                    ("samarqand", "Samarqand viloyati"),
                    ("sirdaryo", "Sirdaryo viloyati"),
                    ("surxondaryo", "Surxondaryo viloyati"),
                    ("toshkent_shahar", "Toshkent shahri"),
                    ("toshkent_viloyati", "Toshkent viloyati"),
                    ("xorazm", "Xorazm viloyati"),
                ],
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="city",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="user",
            name="telegram_id",
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
