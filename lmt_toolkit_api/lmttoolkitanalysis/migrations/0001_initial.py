# Generated by Django 4.2.4 on 2023-08-28 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventDocumentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('representation', models.ImageField(null=True, upload_to='./img/')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('sqlite', models.FileField(max_length=255, upload_to='.')),
                ('rebuild', models.CharField(blank=True, max_length=255, null=True)),
                ('tmin', models.IntegerField(blank=True, null=True)),
                ('tmax', models.IntegerField(blank=True, null=True)),
                ('unitMinT', models.CharField(blank=True, max_length=255, null=True)),
                ('unitMaxT', models.CharField(blank=True, max_length=255, null=True)),
                ('deleteFile', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lmt_toolkit_version', models.CharField(max_length=255)),
                ('lmt_toolkit_version_link', models.CharField(blank=True, max_length=255, null=True)),
                ('lmt_toolkit_version_date', models.DateField()),
                ('lmt_toolkit_version_changes', models.TextField(blank=True, null=True)),
                ('lmt_analysis_version', models.CharField(blank=True, max_length=255, null=True)),
                ('lmt_analysis_version_link', models.CharField(blank=True, max_length=255, null=True)),
                ('lmt_analysis_version_changes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Version',
                'verbose_name_plural': 'Versions',
            },
        ),
    ]
