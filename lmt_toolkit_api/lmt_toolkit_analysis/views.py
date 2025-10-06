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
from time import sleep

from django.http import JsonResponse
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_serializer,
)
from rest_framework.views import APIView
from rest_framework import viewsets, status, generics, parsers, permissions
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from . import tasks
from celery.result import AsyncResult
from celery.worker.control import revoke
from django.core.files.base import ContentFile
from .settings import MEDIA_ROOT
from .serializers import *
from .models import File
from django_celery_results import models as celery_models
from celery.worker import control

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

            # add the task to the file object
            new_file.tasks.add(analysisContext)

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

    # def patch(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()


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
    @extend_schema(request=FileIdSerializer)
    def post(self, request):
        print("check reliability")
        serializer = FileIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_id = serializer.validated_data['file_id']
        sqliteFile = File.objects.get(id=file_id)
        print(sqliteFile)
        path_file = sqliteFile.sqlite.path
        # path_file = sqliteFile.path
        print(path_file)
        try:
            print("into try")
            reliabilityContext = tasks.getReliability.delay(path_file, deleteFile=False, file_id=file_id)
            # reliabilityContext = tasks.getTest.delay()

            sleep(1)

            print("after")


            task_id = str(reliabilityContext.task_id)
            myTask = celery_models.TaskResult.objects.get(task_id=task_id)
            print("task get")
            sqliteFile.tasks.add(myTask)
            print(f"task id {task_id}")

            # return JsonResponse({'filename': reliabilityContext})
            return JsonResponse({'filename': sqliteFile.file_name, 'task_id': task_id, 'path_file': path_file})
        except Exception as e:
            return JsonResponse({f'{e} Error': 'An error occurs during the reliability check'})


class LogInfoAPIView(APIView):
    @extend_schema(request=FileIdSerializer)
    def post(self, request):
        print("logInfoAPIView")
        serializer = FileIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_id = serializer.validated_data['file_id']
        sqliteFile = File.objects.get(id=file_id)
        path_file = sqliteFile.sqlite.path
        try:
            logInfo = tasks.getLogInfoTask.delay(file=path_file, file_id=file_id)
            sleep(1)
            task_id = str(logInfo.task_id)
            myTask = celery_models.TaskResult.objects.get(task_id=task_id)
            sqliteFile.tasks.add(myTask)
            return JsonResponse({'task_id': task_id})
        except Exception as e:
            return JsonResponse({f'{e} Error': 'An error occurs during the log export'})


class SaveAnimalInfoAPIView(APIView):
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
            sleep(1)
            task_id = str(animalInfoContext.task_id)
            myTask = celery_models.TaskResult.objects.get(task_id=task_id)
            sqliteFile.tasks.add(myTask)

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
            rebuildContext = tasks.rebuildSQLite.delay(path_file, file_id, version="LMT-toolkit "+version.lmt_toolkit_version)
            sleep(1)
            task_id = str(rebuildContext.task_id)
            myTask = celery_models.TaskResult.objects.get(task_id=task_id)
            sqliteFile.tasks.add(myTask)
            return JsonResponse({'filename': sqliteFile.file_name, 'task_id': task_id, 'path_file': path_file})
        except:
            return JsonResponse({'Error': 'An error occurs during the rebuild'})


class RebuildNightEventAPIView(APIView):
    def post(self, request):
        version = Version.objects.latest('id')
        file_id = int(request.data['file_id'])
        sqliteFile = File.objects.get(id=file_id)
        path_file = sqliteFile.sqlite.path
        try:
            rebuildNightContext = tasks.buildNightEventTask.delay(file=path_file, startHour=request.data['startHour'], endHour=request.data['endHour'], version="LMT-toolkit "+version.lmt_toolkit_version)
            sleep(1)
            task_id = str(rebuildNightContext.task_id)
            myTask = celery_models.TaskResult.objects.get(task_id=task_id)
            sqliteFile.tasks.add(myTask)
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
            sleep(1)
            task_id = str(analysisContext.task_id)
            myTask = celery_models.TaskResult.objects.get(task_id=task_id)
            sqliteFile.tasks.add(myTask)
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


class DistancePerTimeBinAPIView(APIView):
    def post(self, request):
        version = Version.objects.latest('id')
        file_id = int(request.data['file_id'])
        sqliteFile = File.objects.get(id=file_id)
        path_file = sqliteFile.sqlite.path
        timeBin = int(request.data['timeBin'])
        try:
            activityPerTimeBin = tasks.activityPerTimeBin.delay(path_file, timeBin=timeBin)
            sleep(1)
            task_id = str(activityPerTimeBin.task_id)
            myTask = celery_models.TaskResult.objects.get(task_id=task_id)
            sqliteFile.tasks.add(myTask)
            return JsonResponse({'filename': sqliteFile.file_name, 'task_id': task_id, 'path_file': path_file})
        except:
            return JsonResponse({'Error': 'An error occurs during the activity analysis'})


class StopCeleryTask(APIView):
    def post(self, request):
        task_id = request.data['task_id']
        try:
            print(f"revoke tasks {task_id}")
            # control.revoke(task_id, terminate=True)
            AsyncResult(task_id).revoke(terminate=True)
            # AsyncResult.purge()
            # revoke(task_id, terminate=True)
            return JsonResponse({'task_id': task_id, 'result': "task revoked"})
        except Exception as e:
            return JsonResponse({f'{e} Error': 'An error occurs during the task revocation'})


class PresetViewSet(viewsets.ModelViewSet):
    queryset = Preset.objects.all()
    serializer_class = PresetSerializer


class QualityControlAPIView(APIView):
    """
    To get the quality control of a sqlite file
    """
    serializer_class = FileIdSerializer
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="file_id", description="file id", required=True, type=int
            ),
        ]
    )
    def get(self, request):
        print("get QualityControlResults")
        print(request.GET.get('file_id'))
        try:
            serializer = FileIdSerializer(data = {'file_id': request.GET.get('file_id')})
            serializer.is_valid(raise_exception=True)
            file_id = serializer.validated_data['file_id']
            file = File.objects.get(id=file_id)
            quality_control_results = QualityControl.objects.get(file=file)
            print(quality_control_results.version)
            return JsonResponse({'file_id': file_id, 'version': str(quality_control_results.version),
                                 'quality control': quality_control_results.quality_control})
        except Exception as e:
            return JsonResponse({f'{e} Error': 'Cannot get the quality control results', 'quality control': 'No data'})

    def post(self, request):
        """
        request must have a file_id and a results in a json type
        """
        print("post QualityControlResult")
        try:
            serializer_file_id = FileIdSerializer(data={'file_id': request.data['file_id']})
            serializer_file_id.is_valid(raise_exception=True)
            file_id = serializer_file_id.validated_data['file_id']
            # file = File.objects.get(id=file_id)
            version = Version.objects.latest('id').id

            serializer = QualityControlSerializer(data={'file': file_id, 'version': version,
                                                  'quality_control': request.data['quality_control']})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse({'response': '[View] Quality control saved'})
        except Exception as e:
            print(e)
            return JsonResponse({f'{e} Error': 'Cannot post the quality control results'})
