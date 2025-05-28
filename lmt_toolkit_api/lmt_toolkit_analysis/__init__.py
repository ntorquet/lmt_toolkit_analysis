'''
Created by Nicolas Torquet at 24/11/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
'''


import os
import sys

from .celery import app as celery_app

__all__ = ('celery_app',)


def manage():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lmt_toolkit_analysis.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)