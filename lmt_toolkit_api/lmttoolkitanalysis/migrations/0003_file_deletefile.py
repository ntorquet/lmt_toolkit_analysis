# Generated by Django 4.0.2 on 2023-02-14 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmttoolkitanalysis', '0002_file_tmax_file_tmin_file_unitmaxt_file_unitmint'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='deleteFile',
            field=models.BooleanField(default=False),
        ),
    ]