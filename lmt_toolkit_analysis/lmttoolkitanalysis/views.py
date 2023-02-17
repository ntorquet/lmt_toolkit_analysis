'''
Created by Nicolas Torquet at 12/07/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
'''

import json
import os
from pathlib import Path

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import viewsets, status, generics, parsers, permissions
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from . import tasks
from celery.result import AsyncResult
from django.core.files.base import ContentFile
from lmt_toolkit_analysis.settings import MEDIA_ROOT
from .serializers import *


from .methods import getReliability



class ReadFileAPIView(APIView):
    def post(self, request):
        file = request.FILES['file'].temporary_file_path()
        # file = request.FILES.get('file')
        print(file)
        print(request.FILES['file'])

        # file = request.FILES['file']
        # file = request.FILES['file']
        # with open('/media/temp/%s'%(request.FILES['file'].name), 'wb+') as destination:
        #     for chunk in file.chunks():
        #         destination.write(chunk)


        # print(destination)
        file_name = request.FILES['file'].name
        print(file_name)

        reliabilityContext = tasks.getReliability.delay(request.FILES['file'].temporary_file_path())
        task_id = str(reliabilityContext.task_id)

        # return JsonResponse({'response': "All good", 'filename': file_name, 'reliabilityContext': reliabilityContext})
        return JsonResponse({'task_id': task_id, 'file_name': file_name})




class AnalyseLMTFile(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileSerializer

    def create(self, request):
        print('into the post')
        print("before validation")
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            new_file = serializer.save()
            print("it's valid")
            print(serializer.data)
            print(serializer.data.keys())
            file = serializer.data['sqlite']
            file_name = serializer.data['file_name']
            tmin = serializer.data['tmin']
            tmax = serializer.data['tmax']
            unitMinT = serializer.data['unitMinT']
            unitMaxT = serializer.data['unitMaxT']
            deleteFile = serializer.data['deleteFile']
            # tmin = request.data['tmin']
            # tmax = request.data['tmax']
            # unitMinT = request.data['unitMinT']
            # unitMaxT = request.data['unitMaxT']
            file_id = new_file.id
            print(file)
            # path_to_file = os.path(serializer.data['sqlite'])
            # print("*******" + file.path + "*******")
            print(MEDIA_ROOT)
            path_file = MEDIA_ROOT+serializer.data['sqlite'].split("uploaded/")[1]
            print(path_file)
            analysisContext = tasks.getAnalysis.delay(path_file, deleteFile=deleteFile, file_id=file_id, tmin=tmin, tmax=tmax, unitMinT=unitMinT, unitMaxT=unitMaxT)
            #
            task_id = analysisContext.task_id

            serializer.data['filename']: file_name
            serializer.data['task_id']: task_id
            print(task_id)
            return JsonResponse({'filename': file_name, 'task_id': task_id, 'path_file': path_file})
        else:
            return JsonResponse({'error': 'There was a problem with the data'})



class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class ReliabilityLMTFile(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileSerializer

    def create(self, request):
        print('into the post')
        print("before validation")
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            new_file = serializer.save()
            print("it's valid")
            print(serializer.data)
            print(serializer.data.keys())
            file = serializer.data['sqlite']
            file_name = serializer.data['file_name']
            file_id = new_file.id
            print(file)
            # path_to_file = os.path(serializer.data['sqlite'])
            # print("*******" + file.path + "*******")
            print(MEDIA_ROOT)
            path_file = MEDIA_ROOT+serializer.data['sqlite'].split("uploaded/")[1]
            print(path_file)
            reliabilityContext = tasks.getReliability.delay(path_file, deleteFile=True, file_id=file_id)
            #
            task_id = reliabilityContext.task_id

            serializer.data['filename']: file_name
            serializer.data['task_id']: task_id
            print(task_id)
            return JsonResponse({'filename': file_name, 'task_id': task_id, 'path_file': path_file})
        else:
            return JsonResponse({'error': 'There was a problem with the data'})



