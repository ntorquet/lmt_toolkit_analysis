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

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            new_file = serializer.save()
            file_id = new_file.id
            file_name = new_file.file_name
            return JsonResponse({'filename': file_name, 'file_id': file_id})
        else:
            return JsonResponse({'error': 'There was a problem with the data'})


# class FileUpdateRebuild(generics.UpdateAPIView):
#     queryset = File.objects.all()
#     serializer_class = FileSerializer
#
#     def update(self, request):
#         instance = self.get_object()
#         instance.rebuild = request.data.get("rebuild")
#         instance.save()
#
#         serializer = self.get_serializer(instance)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#
#         return JsonResponse({"Rebuild message": "done"})

class CheckReliabilityAPIView(APIView):
    def post(self, request):
        file_id = int(request.data['file_id'])
        sqliteFile = File.objects.get(id=file_id)
        path_file = sqliteFile.sqlite.path
        print(path_file)
        try:
            reliabilityContext = tasks.getReliability.delay(path_file, deleteFile=False, file_id=file_id)
            # #
            task_id = reliabilityContext.task_id
            print(task_id)
            return JsonResponse({'filename': sqliteFile.file_name, 'task_id': task_id, 'path_file': path_file})
        except:
            return JsonResponse({'Error': 'An error occurs during the reliability check'})


class SaveAnimalInfoView(APIView):
    def post(self, request):
        print("into save animal info view")

        version = Version.objects.latest('id')
        print(str(version.lmt_toolkit_version))
        # data = json.loads(request.body)
        file_id = int(request.data['file_id'])
        sqliteFile = File.objects.get(id=file_id)
        path_file = sqliteFile.sqlite.path

        print(str(request.data['animalsInfo']))
        print(type(json.loads(request.data['animalsInfo'])))
        # data = {'file': path_file,  'animalsInfo': json.load(request.data['animalsInfo'].body.decode('utf-8'))}
        animalDict =  {'file': path_file,  'animalsInfo': json.loads(request.data['animalsInfo']), 'version': "LMT-toolkit "+version.lmt_toolkit_version}
        try:
            animalInfoContext = tasks.saveAnimalInfoTask.delay(animalDict)
            # #
            task_id = animalInfoContext.task_id
            print(task_id)
            return JsonResponse({'task_id': task_id})
        except:
            return JsonResponse({'Error': 'An error occurs during the saving process'})


class RebuildSqliteAPIView(APIView):
    def post(self, request):
        version = Version.objects.latest('id')
        file_id = int(request.data['file_id'])
        sqliteFile = File.objects.get(id=file_id)
        path_file = sqliteFile.sqlite.path
        try:
            rebuildContext = tasks.rebuildSQLite.delay(path_file, file_id, version= "LMT-toolkit "+version.lmt_toolkit_version)
            # #
            task_id = rebuildContext.task_id
            print(task_id)
            return JsonResponse({'filename': sqliteFile.file_name, 'task_id': task_id, 'path_file': path_file})
        except:
            return JsonResponse({'Error': 'An error occurs during the rebuild'})


class ExtractAnalysisAPIView(APIView):
    def post(self, request):
        version = Version.objects.latest('id')
        file_id = int(request.data['file_id'])
        sqliteFile = File.objects.get(id=file_id)
        path_file = sqliteFile.sqlite.path
        tmin = int(request.data['tmin'])
        unitMinT = request.data['unitMinT']
        tmax = int(request.data['tmax'])
        unitMaxT = request.data['unitMaxT']
        try:
            analysisContext = tasks.analyseProfileFromStartTimeToEndTime.delay(path_file,  tmin =tmin , tmax = tmax, unitMinT = unitMinT, unitMaxT = unitMaxT)
            # #
            task_id = analysisContext.task_id
            print(task_id)
            return JsonResponse({'filename': sqliteFile.file_name, 'task_id': task_id, 'path_file': path_file})
        except:
            return JsonResponse({'Error': 'An error occurs during the rebuild'})




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



class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer


class EventDocumentationViewSet(viewsets.ModelViewSet):
    queryset = EventDocumentation.objects.all()
    serializer_class = EventDocumentationSerializer

