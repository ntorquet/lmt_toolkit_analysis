'''
Created by Nicolas Torquet at 12/07/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
'''

from django.db import models
import os


class File(models.Model):
    file_name = models.CharField(max_length=255)
    sqlite = models.FileField(upload_to='.', max_length=255)
    tmin = models.IntegerField(null=True, blank=True)
    tmax = models.IntegerField(null=True, blank=True)
    unitMinT = models.CharField(max_length=255, null=True, blank=True)
    unitMaxT = models.CharField(max_length=255, null=True, blank=True)
    deleteFile = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name

    def delete(self):
        if os.path.isfile(self.sqlite.path):
            os.remove(self.sqlite.path)

        super().delete()

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'


class Version(models.Model):
    lmt_toolkit_version = models.CharField(max_length=255)
    lmt_toolkit_version_link = models.CharField(max_length=255, null=True, blank=True)
    lmt_toolkit_version_date = models.DateField()
    lmt_toolkit_version_changes = models.TextField(null=True, blank=True)
    lmt_analysis_version = models.CharField(max_length=255, null=True, blank=True)
    lmt_analysis_version_link = models.CharField(max_length=255, null=True, blank=True)
    lmt_analysis_version_changes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.lmt_toolkit_version

    class Meta:
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'

class EventDocumentation(models.Model):
    name = models.CharField(max_length=255)
    representation = models.ImageField(upload_to='./img/', height_field=None, width_field=None, null=True,)
    description = models.TextField(null=True, blank=True)