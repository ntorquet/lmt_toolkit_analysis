'''
Created by Nicolas Torquet at 12/07/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
'''

from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField
from .models import *
from django_celery_results import models as celery_models


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = celery_models.TaskResult
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = File
        fields = '__all__'


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'


class EventDocumentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDocumentation
        fields = '__all__'


class FileIdSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()


class QualityControlSerializer(serializers.ModelSerializer):
    version = VersionSerializer(read_only=True)

    class Meta:
        model = QualityControl
        fields = '__all__'


class MetadataFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetadataField
        fields = '__all__'


class MetadataSerializer(serializers.ModelSerializer):
    metadata_fields = MetadataFieldSerializer(many=True)

    class Meta:
        model = Metadata
        fields = '__all__'


class PresetSerializer(serializers.ModelSerializer):
    metadata_fields = MetadataFieldSerializer(many=True)

    class Meta:
        model = Preset
        fields = '__all__'


class AnalysisPresetSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializer(many=True)

    class Meta:
        model = AnalysisPreset
        fields = '__all__'

