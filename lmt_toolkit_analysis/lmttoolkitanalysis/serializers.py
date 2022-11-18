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

class FileSerializer(serializers.ModelSerializer):
    # tmin = TssUpdateExtraVarsSerializer(required=True)
    # tmax = TssUpdateExtraVarsSerializer(required=True)
    # unitMinT = TssUpdateExtraVarsSerializer(required=True)
    # unitMaxT = TssUpdateExtraVarsSerializer(required=True)
    class Meta:
        model = File
        fields = '__all__'