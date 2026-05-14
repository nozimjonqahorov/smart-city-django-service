from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("incidents", "0006_alter_feedback_incident"),
    ]

    operations = [
        migrations.AddField(
            model_name="incident",
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
            model_name="incident",
            name="city",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddIndex(
            model_name="incident",
            index=models.Index(fields=["region"], name="incidents_i_region_abe325_idx"),
        ),
        migrations.AddIndex(
            model_name="incident",
            index=models.Index(fields=["city"], name="incidents_i_city_5c91f3_idx"),
        ),
    ]
