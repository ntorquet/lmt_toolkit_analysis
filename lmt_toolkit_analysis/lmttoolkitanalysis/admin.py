'''
Created by Nicolas Torquet at 23/11/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
'''

from django.contrib import admin

from .models import *

admin.site.register(File)
admin.site.register(Version)

