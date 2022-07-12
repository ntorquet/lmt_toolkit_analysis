from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField
from .models import *

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'