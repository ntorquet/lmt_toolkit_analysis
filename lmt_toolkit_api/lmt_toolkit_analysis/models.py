'''
Created by Nicolas Torquet at 12/07/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
'''

from django.db import models
from django_celery_results import models as celery_models
import os


class File(models.Model):
    file_name = models.CharField(max_length=255)
    sqlite = models.FileField(upload_to='.', max_length=255)
    rebuild = models.CharField(max_length=255, null=True, blank=True)
    tmin = models.IntegerField(null=True, blank=True)
    tmax = models.IntegerField(null=True, blank=True)
    unitMinT = models.CharField(max_length=255, null=True, blank=True)
    unitMaxT = models.CharField(max_length=255, null=True, blank=True)
    tasks = models.ManyToManyField(celery_models.TaskResult, related_name="file_to_celery_tasks", blank=True)

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Event Documentation'
        verbose_name_plural = 'Event Documentations'


class QualityControl(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    version = models.ForeignKey(Version, on_delete=models.SET_NULL, blank=True, null=True)
    quality_control = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = 'Quality control'
        verbose_name_plural = 'Quality control'


class MetadataField(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, null=True, blank=True)
    unit = models.CharField(max_length=255, null=True, blank=True)
    group = models.IntegerField(null=True, blank=True) # the group allows to regroup fields in the frontend forms

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'MetadataField'
        verbose_name_plural = 'MetadataFields'


class Metadata(models.Model):
    metadata_field = models.ForeignKey(MetadataField, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Metadata'
        verbose_name_plural = 'Metadata'
    

class Preset(models.Model):
    preset_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    metadata_field = models.ManyToManyField(MetadataField, related_name="preset_to_metadata_field", blank=True)

    def __str__(self):
        return self.preset_name

    class Meta:
        verbose_name = 'Preset'
        verbose_name_plural = 'Presets'


class Results(models.Model):
    preset = models.ForeignKey(Preset, on_delete=models.SET_NULL, blank=True, null=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    version = models.ForeignKey(Version, on_delete=models.SET_NULL, blank=True, null=True)
    metadata = models.ManyToManyField(Metadata, related_name="results_to_metadata", blank=True)
    results = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = 'Results'
        verbose_name_plural = 'Results'
