'''
Created by Nicolas Torquet at 12/07/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
'''

from django.db import models


class File(models.Model):
    file_name = models.CharField(max_length=255)
    sqlite = models.FileField(upload_to='uploaded/', max_length=255)
    tmin = models.IntegerField(null=True, blank=True)
    tmax = models.IntegerField(null=True, blank=True)
    unitMinT = models.CharField(max_length=255, null=True, blank=True)
    unitMaxT = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'