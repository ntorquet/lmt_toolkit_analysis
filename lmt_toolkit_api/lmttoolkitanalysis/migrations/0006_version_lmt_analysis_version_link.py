# Generated by Django 4.0.2 on 2023-03-20 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmttoolkitanalysis', '0005_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='lmt_analysis_version_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]