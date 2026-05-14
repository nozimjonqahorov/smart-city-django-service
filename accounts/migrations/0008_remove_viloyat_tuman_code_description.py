from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_user_region'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tuman',
            name='code',
        ),
        migrations.RemoveField(
            model_name='tuman',
            name='description',
        ),
        migrations.RemoveField(
            model_name='viloyat',
            name='code',
        ),
        migrations.RemoveField(
            model_name='viloyat',
            name='description',
        ),
        migrations.AlterUniqueTogether(
            name='tuman',
            unique_together={('viloyat', 'name')},
        ),
    ]
