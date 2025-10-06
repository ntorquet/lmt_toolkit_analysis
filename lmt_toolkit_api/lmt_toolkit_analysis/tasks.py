'''
Created by Nicolas Torquet at 12/07/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
'''
import math
import os


from .celery import app
from celery import shared_task
from celery_progress.backend import ProgressRecorder


from .LMT_v1_0_7.scripts.Rebuild_All_Events import process
from .LMT_v1_0_7.lmtanalysis.TaskLogger import TaskLogger
from .LMT_v1_0_7.scripts.TimeLineActivity import extractActivityPerAnimalWholeExperiment
from .LMT_v1_0_7.lmtanalysis import BuildEventApproachContact, BuildEventOtherContact, BuildEventPassiveAnogenitalSniff, BuildEventHuddling, BuildEventTrain3, BuildEventTrain4, BuildEventTrain2, BuildEventFollowZone, BuildEventRear5, BuildEventCenterPeripheryLocation, BuildEventRearCenterPeriphery, BuildEventFloorSniffing, BuildEventSocialApproach, BuildEventSocialEscape, BuildEventApproachContact,BuildEventOralOralContact, BuildEventApproachRear, BuildEventGroup2, BuildEventGroup3, BuildEventGroup4, BuildEventOralGenitalContact, BuildEventStop, BuildEventWaterPoint, BuildEventMove, BuildEventGroup3MakeBreak, BuildEventGroup4MakeBreak, BuildEventSideBySide, BuildEventSideBySideOpposite, BuildEventDetection, BuildDataBaseIndex, BuildEventWallJump, BuildEventSAP, BuildEventOralSideSequence, CheckWrongAnimal, CorrectDetectionIntegrity, BuildEventNest4, BuildEventNest3, BuildEventGetAway
from psutil import virtual_memory
import sys
import traceback
from .LMT_v1_0_7.lmtanalysis.EventTimeLineCache import flushEventTimeLineCache,\
    disableEventTimeLineCache
# from .LMT_v1_0_7.experimental.Animal_LMTtoolkit import *
from .LMT_v1_0_7.experimental.Animal_LMTtoolkit import AnimalPoolToolkit as AnimalPool
from .LMT_v1_0_7.lmtanalysis.Event import *
from .LMT_v1_0_7.lmtanalysis.Measure import *

from .LMT_v1_0_7.lmtanalysis.Util import getAllEvents

from .LMT_v1_0_7.lmtanalysis.EventTimeLineCache import EventTimeLineCached
from .LMT_v1_0_7.lmtanalysis.AnimalType import AnimalType
from .LMT_v1_0_7.experimental.NightRebuilder import buildNightEvent

from .methods import *
from .models import File
from datetime import date
import requests
import json
from .methods import *
from .settings import MEDIA_ROOT, MEDIA_URL
from django.urls import reverse
from django.conf import settings

# import to analyse LMT_v1_0_3 data
import sqlite3




timeUnit = {
    'frame(s)': 1,
    'second(s)': 30,
    'minute(s)': 30*60,
    'hour(s)': 30*60*60,
    'day(s)': 30*60*60*24,
    'week(s)': 30*60*60*24*7,
}

''' time window to compute the events. '''
windowT = 1*oneDay

USE_CACHE_LOAD_DETECTION_CACHE = True


def setAnimalType( aType ):
    global animalType
    animalType = aType


class FileProcessException(Exception):
    pass


def flushEvents( connection, eventClassList):

    print("Flushing events...")

    for ev in eventClassList:

        chrono = Chronometer( "Flushing event " + str(ev) )
        ev.flush( connection );
        chrono.printTimeInS()


def processTimeWindow( connection, file, currentMinT, currentMaxT, eventClassList, progress_recorder, lengthProcess, currentProcessLenght):

    setAnimalType( AnimalType.MOUSE )
    print(f"--- tasks process timeWindow animalType {animalType} ---")
    CheckWrongAnimal.check( connection, tmin=currentMinT, tmax=currentMaxT )

    # Warning: enabling this process (CorrectDetectionIntegrity) will alter the database permanently
    # CorrectDetectionIntegrity.correct( connection, tmin=0, tmax=maxT )

    # BuildEventDetection.reBuildEvent( connection, file, tmin=currentMinT, tmax=currentMaxT )

    animalPool = None

    flushEventTimeLineCache()

    if ( USE_CACHE_LOAD_DETECTION_CACHE ):
        print("Caching load of animal detection...")
        animalPool = AnimalPoolToolkit()
        animalPool.loadAnimals(connection)
        animalPool.loadDetection(start=currentMinT, end=currentMaxT)
        print("Caching load of animal detection done.")

    for ev in eventClassList:
        progress_recorder.set_progress(currentProcessLenght, lengthProcess, f'{ev}')
        chrono = Chronometer(str(ev))
        print(f"------------- {ev} ANIMALTYPE: {animalType} ------------")
        ev.reBuildEvent(connection, file, tmin=currentMinT, tmax=currentMaxT, pool=animalPool, animalType=animalType )
        chrono.printTimeInS()
        currentProcessLenght += 1

    return currentProcessLenght



@shared_task(bind=True)
def getLogInfoTask(self, file, file_id):
    '''
    :param file: the SQLite LMT_v1_0_3 file
    :return: extracted log info from file
    '''
    print("task getLogInfoTask")
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 2, f'[Get log info] Starting')
    connection = create_connection(file)
    progress_recorder.set_progress(1, 2, f'[Get log info] File connected')
    logInfo = getLogInfo(connection, file_id)
    progress_recorder.set_progress(2, 2, f'[Get log info] Log info extracted')
    connection.close()

    return logInfo


@shared_task(bind=True)
def getAnalysis(self, file, deleteFile = False, file_id = "", tmin = 0, tmax = -1, unitMinT = None, unitMaxT = None):
    '''
    :param file: the SQLite LMT_v1_0_3 file
    :return: extracted data
    '''
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 12, f'Starting')
    # file = request.FILES.get('file').temporary_file_path()
    # filename = request.FILES['file'].name

    # experiment_form = addExperiment()
    # experiment_form.fields['name_experiment'].initial = filename[:-7]
    # experiment_form['xp_file_name'].initial = filename
    # group_form = addGroup()
    # protocol_form = addProtocol()
    # project_form = addProject()
    # print('file:' + file)
    # print('file exists:' + str(os.path.exists(file)))

    # connection = sqlite3.connect(file)
    # from .methods import create_connection
    connection = create_connection(file)
    print('File: '+file)
    progress_recorder.set_progress(1, 12, f'File loaded')
    print(connection)
    # from .methods import findMiceInSQLiteFile

    mice = findMiceInSQLiteFile(connection)
    progress_recorder.set_progress(2, 12, f'Mice identified')
    # from .methods import findStartandEndInSQLiteFile
    startAndEnd = findStartandEndInSQLiteFile(connection)

    progress_recorder.set_progress(3, 12, f'Time information found')
    # from .methods import getSensorInSQLiteFile
    sensors = getSensorInSQLiteFile(connection)
    progress_recorder.set_progress(4, 12, f'Sensors information done')
    # from .methods import checkOmittedFrames
    omissions = checkOmittedFrames(connection)
    progress_recorder.set_progress(5, 12, f'Omissions calculated')
    # from .methods import getAnimalDetection
    list_detection_animals = getAnimalDetection(connection)
    progress_recorder.set_progress(6, 12, f'Animal detection done')
    # from .methods import checkAnimalDetectionOmissions
    percentageOfDetection = checkAnimalDetectionOmissions(omissions['theoricalNumberOfFrame'],
                                                          omissions['nbFramesRecorded'], list_detection_animals)
    # from .methods import getRFIDdetections
    rfid_detection_animals = getRFIDdetections(connection)
    progress_recorder.set_progress(7, 12, f'RFID detection loaded')
    # from .methods import getRFIDmatchDetections
    rfidmatch_detection_animals = getRFIDmatchDetections(connection)
    progress_recorder.set_progress(8, 12, f'RFID match done')
    # from .methods import getRFIDmismatchDetections
    rfidmismatch_detection_animals = getRFIDmismatchDetections(connection)
    progress_recorder.set_progress(9, 12, f'RFID mismatch done')

    infoFromFile = {'mice': mice, 'startAndEnd': startAndEnd, 'sensors': sensors, 'omissions': omissions, 'list_detection_animals': list_detection_animals,
                'rfid_detection_animals': rfid_detection_animals, 'rfidmatch_detection_animals': rfidmatch_detection_animals,
                'rfidmismatch_detection_animals': rfidmismatch_detection_animals,
                'percentageOfDetection': percentageOfDetection}

    # rfid_detection_animals = getRFIDdetections(connection)
    # rfidmatch_detection_animals = getRFIDmatchDetections(connection)
    # rfidmismatch_detection_animals = getRFIDmismatchDetections(connection)
    #
    # 'mice': mice, 'startAndEnd': startAndEnd, 'sensors': sensors, 'omissions': omissions, 'list_detection_animals': list_detection_animals,
    # 'rfid_detection_animals': rfid_detection_animals, 'rfidmatch_detection_animals': rfidmatch_detection_animals,
    # 'rfidmismatch_detection_animals': rfidmismatch_detection_animals,
    # 'percentageOfDetection': percentageOfDetection


    # version of the reliability methods
    reliability_version = 'v0.0'

    mice = infoFromFile['mice']

    numberOfMice = len(mice)

    xpDates = infoFromFile['startAndEnd']
    startXp = xpDates['start_experiment']
    endXp = xpDates['end_experiment']

    # omissions
    realDurationInSeconds = infoFromFile['omissions']['realDurationInSeconds']
    realDurationInMinutes = infoFromFile['omissions']['realDurationInMinutes']
    realDurationInHours = infoFromFile['omissions']['realDurationInHours']
    realDurationInDays = infoFromFile['omissions']['realDurationInDays']
    theoricalNumberOfFrame = infoFromFile['omissions']['theoricalNumberOfFrame']
    nbFramesRecorded = infoFromFile['omissions']['nbFramesRecorded']
    nbFramesRecordedInSeconds = infoFromFile['omissions']['nbFramesRecordedInSeconds']
    nbFramesRecordedInMinutes = infoFromFile['omissions']['nbFramesRecordedInMinutes']
    nbFramesRecordedInHours = infoFromFile['omissions']['nbFramesRecordedInHours']
    nbFramesRecordedInDays = infoFromFile['omissions']['nbFramesRecordedInDays']
    durationExpFromFrame = infoFromFile['omissions']['durationExpFromFrame']
    nbOmittedFrames = infoFromFile['omissions']['nbOmittedFrames']
    percentageOfOmittedFrames = infoFromFile['omissions']['percentageOfOmittedFrames']
    nbOmittedSeconds = infoFromFile['omissions']['nbOmittedSeconds']
    nbOmittedMinutes = infoFromFile['omissions']['nbOmittedMinutes']
    nbOmittedHours = infoFromFile['omissions']['nbOmittedHours']
    nbOmittedDays = infoFromFile['omissions']['nbOmittedDays']
    # message depending of percentage of omissions
    if percentageOfOmittedFrames < 0:
        omissionColor = "red"
        omissionIcon = "times icon"
        omissionInformation = "There are more recorded frames than expected: there is a problem with the acquisition. This file should not be used."
    elif percentageOfOmittedFrames < 0.08:
        omissionColor = "green"
        omissionIcon = "check icon"
        omissionInformation = "The number of dropped frames is limited"
    elif percentageOfOmittedFrames < 1:
        omissionColor = "orange"
        omissionIcon = "exclamation icon"
        omissionInformation = "The number of frames dropped is acceptable."
    else:
        omissionColor = "red"
        omissionIcon = "times icon"
        omissionInformation = "The number of dropped frames is too high."

    # animal detection check
    list_detection_animals = infoFromFile['list_detection_animals']
    percentageOfDetection = infoFromFile['percentageOfDetection']

    aboutDetections = {}
    for linePercentageOfDetection in percentageOfDetection:
        for lineList_detection_animals in list_detection_animals:
            if linePercentageOfDetection['animalId'] == lineList_detection_animals['animalId']:
                aboutDetections[linePercentageOfDetection['animalId']] = {
                    'animalId': lineList_detection_animals['animalId'],
                    'nbDetection': lineList_detection_animals['nbDetection'],
                    'detectionPercentTheoricalFrames': linePercentageOfDetection['detectionPercentTheoricalFrames'],
                    'detectionPercentRecordedFrames': linePercentageOfDetection['detectionPercentRecordedFrames'],
                    'detectionPercentTheoricalFramesColor': linePercentageOfDetection['detectionPercentTheoricalFramesColor'],
                    'detectionPercentRecordedFramesColor': linePercentageOfDetection['detectionPercentRecordedFramesColor'],
                    'messageDetectionFrameColor': linePercentageOfDetection['messageDetectionFrameColor'],
                    'messageDetectionFramesIcon': linePercentageOfDetection['messageDetectionFramesIcon'],
                    'messageDetectionFrame': linePercentageOfDetection['messageDetectionFrame']
                }

    reliabilityContext = {'reliability_version': reliability_version, 'numberOfMice': numberOfMice,
                   'mouse': mice, 'xpDates': xpDates, 'start_experiment': startXp, 'end_experiment': endXp,
                   'startXp': startXp, 'endXp': endXp, 'realDurationInSeconds': realDurationInSeconds,
                   'realDurationInMinutes': realDurationInMinutes, 'realDurationInHours': realDurationInHours,
                   'realDurationInDays': realDurationInDays, 'theoricalNumberOfFrame': theoricalNumberOfFrame,
                   'nbFramesRecorded': nbFramesRecorded, 'nbFramesRecordedInSeconds': nbFramesRecordedInSeconds,
                   'nbFramesRecordedInMinutes': nbFramesRecordedInMinutes,
                   'nbFramesRecordedInHours': nbFramesRecordedInHours,
                   'nbFramesRecordedInDays': nbFramesRecordedInDays, 'durationExpFromFrame': durationExpFromFrame,
                   'nbOmittedFrames': nbOmittedFrames, 'percentageOfOmittedFrames': percentageOfOmittedFrames,
                   'nbOmittedSeconds': nbOmittedSeconds, 'nbOmittedMinutes': nbOmittedMinutes,
                   'nbOmittedHours': nbOmittedHours, 'nbOmittedDays': nbOmittedDays,
                   'omissionColor': omissionColor, 'omissionIcon': omissionIcon,
                   'omissionInformation': omissionInformation, 'list_detection_animals': list_detection_animals, 'percentageOfDetection': percentageOfDetection,
                    'aboutDetections': aboutDetections,
                   # 'rfid_detection_animals': rfid_detection_animals,
                   # 'rfidmatch_detection_animals': rfidmatch_detection_animals,
                   # 'rfidmismatch_detection_animals': rfidmismatch_detection_animals
                   }

    rfidDetection = False
    about_rfid_detections = {}
    for mouse in mice:
        if not 'RFID' in mouse['tag_subject']:
            rfidDetection = True
    print(str(rfidDetection))


    if rfidDetection:
        rfid_detection_animals = infoFromFile['rfid_detection_animals']
        rfidmatch_detection_animals = infoFromFile['rfidmatch_detection_animals']
        rfidmismatch_detection_animals = infoFromFile['rfidmismatch_detection_animals']
        print(rfid_detection_animals)
        print(rfidmatch_detection_animals)
        print(rfidmismatch_detection_animals)

        for mouse in rfid_detection_animals.keys():
            if mouse != None:
                if (rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] + rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection'] == 0):
                    about_rfid_detections[mouse] = {
                        'animalId': mouse,
                        'nbRFIDdetection': rfid_detection_animals[mouse]['nbRFIDdetection'],
                        'nbRFIDmatchdetection': rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'],
                        'nbRFIDmismatchdetection': rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection'],
                        'match_mismatch_proportion': [0, 0]
                    }
                    reliabilityContext.update(
                        {'rfidDetection': rfidDetection, 'about_rfid_detections': about_rfid_detections,
                         'rfid_detection_animals': rfid_detection_animals,
                         'rfidmatch_detection_animals': rfidmatch_detection_animals,
                         'rfidmismatch_detection_animals': rfidmismatch_detection_animals})
                else:
                    about_rfid_detections[mouse] = {
                        'animalId': mouse,
                        'nbRFIDdetection': rfid_detection_animals[mouse]['nbRFIDdetection'],
                        'nbRFIDmatchdetection': rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'],
                        'nbRFIDmismatchdetection': rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection'],
                        'match_mismatch_proportion': [rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] / (rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] + rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection']) * 100,
                rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection'] / (rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] + rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection']) * 100]
                    }
                reliabilityContext.update({'rfidDetection': rfidDetection, 'about_rfid_detections': about_rfid_detections,
                                           'rfid_detection_animals': rfid_detection_animals,
                                           'rfidmatch_detection_animals': rfidmatch_detection_animals,
                                           'rfidmismatch_detection_animals': rfidmismatch_detection_animals})
    else:
        about_rfid_detections = 'no rfid'
        reliabilityContext.update({'rfidDetection': rfidDetection, 'about_rfid_detections': about_rfid_detections})

    print(about_rfid_detections)

    #
    # rfid_detection_animals = infoFromFile['rfid_detection_animals']
    # rfidmatch_detection_animals = infoFromFile['rfidmatch_detection_animals']
    # rfidmismatch_detection_animals = infoFromFile['rfidmismatch_detection_animals']

    print('Sensors')
    # sensors
    if infoFromFile['sensors'] != "no sensors":
        timeline = infoFromFile['sensors']['timeline']
        temperature = infoFromFile['sensors']['temperature']
        humidity = infoFromFile['sensors']['humidity']
        sound = infoFromFile['sensors']['sound']
        lightvisible = infoFromFile['sensors']['lightvisible']
        lightvisibleandir = infoFromFile['sensors']['lightvisibleandir']
        highTemp = infoFromFile['sensors']['highTemp']
        lowTemp = infoFromFile['sensors']['lowTemp']
        if highTemp == False:
            highTempColor = "green"
            highTempIcon = "check icon"
            highTempInformation = "The temperature didn't exceed 25°C."
        elif highTemp == "high":
            highTempColor = "orange"
            highTempIcon = "sun icon"
            highTempInformation = "The temperature exceeded 25°C during the experiment but didn't reach 26°C."
        else:
            highTempColor = "red"
            highTempIcon = "hotjar icon"
            highTempInformation = "The temperature exceeded 26°C during the experiment."

        if lowTemp == False:
            lowTempColor = "green"
            lowTempIcon = "check icon"
            lowTempInformation = "The temperature wasn't lower than 21°C."
        elif lowTemp == "low":
            lowTempColor = "teal"
            lowTempIcon = "snowflake outline icon icon"
            lowTempInformation = "The temperature was below 21°C but was still above 20°C."
        else:
            lowTempColor = "blue"
            lowTempIcon = "igloo icon"
            lowTempInformation = "The temperature was below 21°C."

        sensors = {'sensors': "sensors", 'temperature': temperature,
                   'timeline': timeline, 'humidity': humidity, 'sound': sound, 'lightvisible': lightvisible,
                   'lightvisibleandir': lightvisibleandir, 'highTemp': highTemp, 'lowTemp': lowTemp,
                   'highTempColor': highTempColor, 'highTempIcon': highTempIcon,
                   'highTempInformation': highTempInformation,
                   'lowTempColor': lowTempColor, 'lowTempIcon': lowTempIcon, 'lowTempInformation': lowTempInformation}
    else:
        sensors = {'sensors': "no sensors"}

    reliabilityContext.update(sensors)


    # about_rfid_detections = {}
    # for mouse in rfid_detection_animals.keys():
    #     # print('rfidmatch_detection_animals '+str(rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection']))
    #     # print('nbRFIDmismatchdetection '+str(rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection']))
    #     about_rfid_detections[mouse] = {
    #         'animalId': mouse,
    #         'nbRFIDdetection': rfid_detection_animals[mouse]['nbRFIDdetection'],
    #         'nbRFIDmatchdetection': rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'],
    #         'nbRFIDmismatchdetection': rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection'],
    #         'match_mismatch_proportion': [rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] / (rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] + rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection']) * 100,
    # rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection'] / (rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] + rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection']) * 100]
    #     }

    # if len(rfid_detection_animals) > 0:
    #     rfidDetection = True
    # else:
    #     rfidDetection = False

    # context = {'numberOfMice': numberOfMice,
    #            'aboutDetections': aboutDetections,
    #             'list_detection_animals': list_detection_animals, 'percentageOfDetection': percentageOfDetection,
    #             'rfid_detection_animals': rfid_detection_animals,
    #             'rfidmatch_detection_animals': rfidmatch_detection_animals,
    #             'rfidmismatch_detection_animals': rfidmismatch_detection_animals,
    #             'about_rfid_detections': about_rfid_detections, 'rfidDetection': rfidDetection
    #         }
    # reliabilityContext.update(context)





    print("************** Analysis **************")
    # analyse all the experiment

    StartEndFrames = getStartEndExperiment(connection)
    if int(tmin) == 0 or unitMinT == None or unitMinT == "null":
        minT = StartEndFrames[0]
    else:
        minT = int(tmin)*timeUnit[unitMinT]
    if tmax == "-" or unitMaxT == None or unitMaxT == "null":
        maxT = StartEndFrames[1]
    else:
        maxT = int(tmax)*timeUnit[unitMaxT]


    # Rebuild_all_event from minT to maxT
    progress_recorder.set_progress(10, 12, f'first analysis done - start Rebuild_all_event')
    process(file, minT, maxT)

    progress_recorder.set_progress(11, 12, f'Rebuild done - compute analysis')


    # Analysis from minT to maxT
    profileData = getDataProfile(connection, minT, maxT, file)
    print("tmin: " + str(tmin))
    print("unitMinT: "+str(unitMinT))
    print("tmax: " + str(tmax))
    print("unitMaxT: "+str(unitMaxT))
    print("minT: "+str(minT))
    print("maxT: "+str(maxT))

    reliabilityContext.update({'profileData': profileData})

    progress_recorder.set_progress(12, 12, f'Analysis done')

    connection.close()

    # deleteFile
    instance = File.objects.get(id=file_id)
    file_id = {'file_id': file_id}
    if deleteFile:
        print("Delete SQLite file")
        print('file id: ' + str(file_id))
        # url_deleteFile = 'http://127.0.0.1:8000/api/files/' + str(file_id['file_id'])
        relative_url = reverse('files-detail', kwargs={'pk': file_id})
        url_deleteFile = f"{settings.API_BASE_URL}{relative_url}"
        # url_deleteFile = 'http://127.0.0.1:8000/api/files/' + str(file_id['file_id'])
        print(url_deleteFile)
        response = requests.delete(url_deleteFile)
        file_url = {'file_url': ''}

    else:
        file_url = {'file_url': MEDIA_URL+str(instance.sqlite)}
        print(MEDIA_URL)
        print('file_url: '+file_url['file_url'])


    reliabilityContext.update(file_id)
    reliabilityContext.update(file_url)

    return reliabilityContext


@shared_task(bind=True)
def rebuildSQLite(self, file, file_id, version):
    '''
    :param file: the SQLite LMT_v1_0_3 file
    :return: job done
    '''

    eventClassList = [
        # BuildEventHuddling,
        BuildEventDetection,
        BuildEventOralOralContact,
        BuildEventOralGenitalContact,
        BuildEventSideBySide,
        BuildEventSideBySideOpposite,
        BuildEventTrain2,
        BuildEventTrain3,
        BuildEventTrain4,
        BuildEventMove,
        BuildEventFollowZone,
        BuildEventRear5,
        BuildEventCenterPeripheryLocation,
        BuildEventRearCenterPeriphery,
        BuildEventSocialApproach,
        BuildEventGetAway,
        BuildEventSocialEscape,
        BuildEventApproachRear,
        BuildEventGroup2,
        BuildEventGroup3,
        BuildEventGroup4,
        BuildEventGroup3MakeBreak,
        BuildEventGroup4MakeBreak,
        BuildEventStop,
        BuildEventWaterPoint,
        BuildEventApproachContact,
        # BuildEventWallJump,
        BuildEventSAP,
        BuildEventOralSideSequence,
        BuildEventNest3,
        BuildEventNest4
    ]

    progress_recorder = ProgressRecorder(self)
    # number of step for progress is evaluated from number of events to rebuild, it will be calculated a bit later
    progress_recorder.set_progress(0, len(eventClassList)+3, f'[Rebuild] Starting')

    connection = create_connection(file)
    print('File: '+file)
    print(connection)
    progress_recorder.set_progress(1, len(eventClassList)+3, f'[Rebuild] File loaded')
    StartEndFrames = getStartEndExperiment(connection)
    minT = StartEndFrames[0]
    maxT = StartEndFrames[1]
    connection.close()

    nbOfTimeWindows = ceil((maxT-minT)/windowT)
    lengthProcess = 4 + len(eventClassList*nbOfTimeWindows)
    print(f"LengthProcess: {lengthProcess}")

    # Rebuild_all_event from minT to maxT
    progress_recorder.set_progress(3, lengthProcess, f'[Rebuild] first analysis done - start Rebuild_all_event')
    currentLenghtProcess = 4

    # process event rebuild one by one
    mem = virtual_memory()
    availableMemoryGB = mem.total / 1000000000
    print( "Total memory on computer: (GB)", availableMemoryGB )

    if availableMemoryGB < 10:
        print( "Not enough memory to use cache load of events.")
        disableEventTimeLineCache()

    chronoFullFile = Chronometer("File " + file)

    connection = sqlite3.connect(file)

    # update missing fields
    try:
        connection = sqlite3.connect(file)
        c = connection.cursor()
        query = "ALTER TABLE EVENT ADD METADATA TEXT";
        c.execute(query)
        connection.commit()

    except:
        print("METADATA field already exists", file)

    BuildDataBaseIndex.buildDataBaseIndex(connection, force=False)
    # build sensor data
    animalPool = AnimalPoolToolkit()
    animalPool.loadAnimals(connection)
    # animalPool.buildSensorData(file)

    currentT = minT

    try:
        flushEvents(connection, eventClassList)

        while currentT < maxT:
            currentMinT = currentT
            currentMaxT = currentT + windowT
            if (currentMaxT > maxT):
                currentMaxT = maxT

            chronoTimeWindowFile = Chronometer(
                "File " + file + " currentMinT: " + str(currentMinT) + " currentMaxT: " + str(currentMaxT));
            currentLenghtProcess = processTimeWindow(connection, file, currentMinT, currentMaxT, eventClassList, progress_recorder, lengthProcess, currentLenghtProcess)
            chronoTimeWindowFile.printTimeInS()

            currentT += windowT

            print(f"currentLengthProcess: {currentLenghtProcess}")

        print("Full file process time: ")
        chronoFullFile.printTimeInS()

        TEST_WINDOWING_COMPUTATION = False

        if (TEST_WINDOWING_COMPUTATION):

            print("*************")
            print("************* TEST START SECTION")
            print("************* Test if results are the same with or without the windowing.")

            # display and record to a file all events found, checking with rolling idA from None to 4. Save nbEvent and total len

            # eventTimeLineList = []
            #
            # eventList = getAllEvents(connection)
            #file = open("outEvent" + str(windowT) + ".txt", "w")
            #file.write("Event name\nnb event\ntotal duration")

            # for eventName in eventList:
            #     print(eventName)
            #     for animal in range(0, 5):
            #         idA = animal
            #         if idA == 0:
            #             idA = None
            #         timeLine = EventTimeLineCached(connection, file, eventName, idA, minFrame=minT, maxFrame=maxT)
            #         eventTimeLineList.append(timeLine)
            #         file.write(timeLine.eventNameWithId + "\t" + str(len(timeLine.eventList)) + "\t" + str(
            #             timeLine.getTotalLength()) + "\n")
            #
            # file.close()

            # plotMultipleTimeLine( eventTimeLineList )

            print("************* END TEST")

        flushEventTimeLineCache()

    except:

        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        error = ''.join('!! ' + line for line in lines)

        t = TaskLogger(connection)
        t.addLog(error)
        flushEventTimeLineCache()

        print(error, file=sys.stderr)

        raise FileProcessException()

    # process(file, minT, maxT)

    connection = create_connection(file)
    t = TaskLogger(connection)
    t.addLog("Rebuild all events", version=version)
    connection.close()

    # update file in database: rebuild field with version number
    # api_url = f"http://127.0.0.1:8000/api/files/{file_id}/"
    relative_url = reverse('files-detail', kwargs={'pk': file_id})
    api_url = f"{settings.API_BASE_URL}{relative_url}"
    print("*********************")
    print(file_id)
    todo = {"rebuild": version}
    response = requests.patch(api_url, json=todo)
    # print(response.json())
    print("*********************")
    print(response.status_code)
    progress_recorder.set_progress(currentLenghtProcess, lengthProcess, f'[Rebuild] Rebuild done - compute analysis')

    return {"message": "Rebuild done"}


@shared_task(bind=True)
def saveAnimalInfoTask(self, data):
    '''
    :param data: contains the SQLite LMT_v1_0_3 file and the info to save
    :return: job done
    '''
    print("in saveAnimalInfoTask")
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 4, f'[Animal info] Starting')
    file = data['file']
    animalsInfo = data ['animalsInfo']
    version = data['version']
    print(version)

    print('File: '+file)
    progress_recorder.set_progress(1, 4, f'[Animal info] File loaded')

    saveAnimalInfo(file, animalsInfo, version)

    progress_recorder.set_progress(3, 4, f'[Animal info] writing into the database')

    progress_recorder.set_progress(4, 4, f'[Animal info] Saving done')

    return {"message": "Saving done"}


@shared_task(bind=True)
def analyseProfileFromStartTimeToEndTime(self, file,  tmin = 0, tmax = -1, unitMinT = None, unitMaxT = None):
    '''
    :param file: the SQLite LMT_v1_0_3 file, tmin and tmax and their units (unitMinT and unitMaxT) as start and end for the analysis
    :return: profile (results of behaviors) for each animal
    '''

    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 2, f'[Profile analysis] Starting')

    connection = create_connection(file)

    StartEndFrames = getStartEndExperiment(connection)
    if int(tmin) == 0 or unitMinT == None or unitMinT == "null" or unitMinT == "":
        minT = StartEndFrames[0]
    else:
        minT = int(tmin)*int(timeUnit[unitMinT])
    if tmax == "-" or unitMaxT == None or unitMaxT == "null" or unitMaxT == "":
        maxT = StartEndFrames[1]
    else:
        maxT = int(tmax)*int(timeUnit[unitMaxT])

    progress_recorder.set_progress(1, 2, f'[Profile analysis] Start and end frames found')

    profileData = getDataProfile(connection, minT, maxT, file)
    # print("tmin: " + str(tmin))
    # print("unitMinT: "+str(unitMinT))
    # print("tmax: " + str(tmax))
    # print("unitMaxT: "+str(unitMaxT))
    # print("minT: "+str(minT))
    # print("maxT: "+str(maxT))

    progress_recorder.set_progress(2, 2, f'[Profile analysis] Analysis done')

    connection.close()

    return profileData


@shared_task(bind=True)
def getTest(self):
    print("coucou")
    return "coucou"

@shared_task(bind=True)
def getReliability(self, file, deleteFile = True, file_id = ""):
    '''
    :param file: the SQLite LMT_v1_0_3 file
    :return: reliability
    '''
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 10, f'[Quality control] Starting')

    connection = create_connection(file)
    print('File: '+file)
    progress_recorder.set_progress(1, 10, f'[Quality control] File loaded')
    print(connection)
    # from .methods import findMiceInSQLiteFile

    mice = findMiceInSQLiteFile(connection)
    progress_recorder.set_progress(2, 10, f'[Quality control] Mice identified')
    # from .methods import findStartandEndInSQLiteFile
    startAndEnd = findStartandEndInSQLiteFile(connection)

    progress_recorder.set_progress(3, 10, f'[Quality control] Time information found')
    # from .methods import getSensorInSQLiteFile
    sensors = getSensorInSQLiteFile(connection)
    progress_recorder.set_progress(4, 10, f'[Quality control] Sensors information done')
    # from .methods import checkOmittedFrames
    omissions = checkOmittedFrames(connection)
    progress_recorder.set_progress(5, 10, f'[Quality control] Omissions calculated')
    # from .methods import getAnimalDetection
    list_detection_animals = getAnimalDetection(connection)
    progress_recorder.set_progress(6, 10, f'[Quality control] Animal detection done')
    # from .methods import checkAnimalDetectionOmissions
    percentageOfDetection = checkAnimalDetectionOmissions(omissions['theoricalNumberOfFrame'],
                                                          omissions['nbFramesRecorded'], list_detection_animals)
    # from .methods import getRFIDdetections
    rfid_detection_animals = getRFIDdetections(connection)
    progress_recorder.set_progress(7, 10, f'[Quality control] RFID detection loaded')
    # from .methods import getRFIDmatchDetections
    rfidmatch_detection_animals = getRFIDmatchDetections(connection)
    progress_recorder.set_progress(8, 10, f'[Quality control] RFID match done')
    # from .methods import getRFIDmismatchDetections
    rfidmismatch_detection_animals = getRFIDmismatchDetections(connection)
    progress_recorder.set_progress(9, 10, f'[Quality control] RFID mismatch done')

    infoFromFile = {'mice': mice, 'startAndEnd': startAndEnd, 'sensors': sensors, 'omissions': omissions, 'list_detection_animals': list_detection_animals,
                'rfid_detection_animals': rfid_detection_animals, 'rfidmatch_detection_animals': rfidmatch_detection_animals,
                'rfidmismatch_detection_animals': rfidmismatch_detection_animals,
                'percentageOfDetection': percentageOfDetection}

    # version of the reliability methods
    reliability_version = 'v0.0'

    mice = infoFromFile['mice']

    numberOfMice = len(mice)

    xpDates = infoFromFile['startAndEnd']
    startXp = xpDates['start_experiment']
    endXp = xpDates['end_experiment']

    # omissions
    realDurationInSeconds = infoFromFile['omissions']['realDurationInSeconds']
    realDurationInMinutes = infoFromFile['omissions']['realDurationInMinutes']
    realDurationInHours = infoFromFile['omissions']['realDurationInHours']
    realDurationInDays = infoFromFile['omissions']['realDurationInDays']
    theoricalNumberOfFrame = infoFromFile['omissions']['theoricalNumberOfFrame']
    nbFramesRecorded = infoFromFile['omissions']['nbFramesRecorded']
    nbFramesRecordedInSeconds = infoFromFile['omissions']['nbFramesRecordedInSeconds']
    nbFramesRecordedInMinutes = infoFromFile['omissions']['nbFramesRecordedInMinutes']
    nbFramesRecordedInHours = infoFromFile['omissions']['nbFramesRecordedInHours']
    nbFramesRecordedInDays = infoFromFile['omissions']['nbFramesRecordedInDays']
    durationExpFromFrame = infoFromFile['omissions']['durationExpFromFrame']
    nbOmittedFrames = infoFromFile['omissions']['nbOmittedFrames']
    percentageOfOmittedFrames = infoFromFile['omissions']['percentageOfOmittedFrames']
    nbOmittedSeconds = infoFromFile['omissions']['nbOmittedSeconds']
    nbOmittedMinutes = infoFromFile['omissions']['nbOmittedMinutes']
    nbOmittedHours = infoFromFile['omissions']['nbOmittedHours']
    nbOmittedDays = infoFromFile['omissions']['nbOmittedDays']
    # message depending of percentage of omissions
    if percentageOfOmittedFrames < 0:
        omissionColor = "red"
        omissionIcon = "times icon"
        omissionInformation = "There are more recorded frames than expected: there is a problem with the acquisition. This file should not be used."
    elif percentageOfOmittedFrames < 0.08:
        omissionColor = "green"
        omissionIcon = "check icon"
        omissionInformation = "The number of dropped frames is limited"
    elif percentageOfOmittedFrames < 1:
        omissionColor = "orange"
        omissionIcon = "exclamation icon"
        omissionInformation = "The number of frames dropped is acceptable."
    else:
        omissionColor = "red"
        omissionIcon = "times icon"
        omissionInformation = "The number of dropped frames is too high."

    # animal detection check
    list_detection_animals = infoFromFile['list_detection_animals']
    percentageOfDetection = infoFromFile['percentageOfDetection']

    aboutDetections = {}
    for linePercentageOfDetection in percentageOfDetection:
        for lineList_detection_animals in list_detection_animals:
            if linePercentageOfDetection['animalId'] == lineList_detection_animals['animalId']:
                aboutDetections[linePercentageOfDetection['animalId']] = {
                    'animalId': lineList_detection_animals['animalId'],
                    'nbDetection': lineList_detection_animals['nbDetection'],
                    'detectionPercentTheoricalFrames': linePercentageOfDetection['detectionPercentTheoricalFrames'],
                    'detectionPercentRecordedFrames': linePercentageOfDetection['detectionPercentRecordedFrames'],
                    'detectionPercentTheoricalFramesColor': linePercentageOfDetection['detectionPercentTheoricalFramesColor'],
                    'detectionPercentRecordedFramesColor': linePercentageOfDetection['detectionPercentRecordedFramesColor'],
                    'messageDetectionFrameColor': linePercentageOfDetection['messageDetectionFrameColor'],
                    'messageDetectionFramesIcon': linePercentageOfDetection['messageDetectionFramesIcon'],
                    'messageDetectionFrame': linePercentageOfDetection['messageDetectionFrame']
                }

    reliabilityContext = {'reliability_version': reliability_version, 'numberOfMice': numberOfMice,
                   'mouse': mice, 'xpDates': xpDates, 'start_experiment': startXp, 'end_experiment': endXp,
                   'startXp': startXp, 'endXp': endXp, 'realDurationInSeconds': realDurationInSeconds,
                   'realDurationInMinutes': realDurationInMinutes, 'realDurationInHours': realDurationInHours,
                   'realDurationInDays': realDurationInDays, 'theoricalNumberOfFrame': theoricalNumberOfFrame,
                   'nbFramesRecorded': nbFramesRecorded, 'nbFramesRecordedInSeconds': nbFramesRecordedInSeconds,
                   'nbFramesRecordedInMinutes': nbFramesRecordedInMinutes,
                   'nbFramesRecordedInHours': nbFramesRecordedInHours,
                   'nbFramesRecordedInDays': nbFramesRecordedInDays, 'durationExpFromFrame': durationExpFromFrame,
                   'nbOmittedFrames': nbOmittedFrames, 'percentageOfOmittedFrames': percentageOfOmittedFrames,
                   'nbOmittedSeconds': nbOmittedSeconds, 'nbOmittedMinutes': nbOmittedMinutes,
                   'nbOmittedHours': nbOmittedHours, 'nbOmittedDays': nbOmittedDays,
                   'omissionColor': omissionColor, 'omissionIcon': omissionIcon,
                   'omissionInformation': omissionInformation, 'list_detection_animals': list_detection_animals, 'percentageOfDetection': percentageOfDetection,
                    'aboutDetections': aboutDetections,
                   # 'rfid_detection_animals': rfid_detection_animals,
                   # 'rfidmatch_detection_animals': rfidmatch_detection_animals,
                   # 'rfidmismatch_detection_animals': rfidmismatch_detection_animals
                   }

    rfidDetection = False
    about_rfid_detections = {}
    for mouse in mice:
        if not 'RFID' in mouse['RFID']:
            rfidDetection = True
    print(str(rfidDetection))


    if rfidDetection:
        rfid_detection_animals = infoFromFile['rfid_detection_animals']
        rfidmatch_detection_animals = infoFromFile['rfidmatch_detection_animals']
        rfidmismatch_detection_animals = infoFromFile['rfidmismatch_detection_animals']
        print(rfid_detection_animals)
        print(rfidmatch_detection_animals)
        print(rfidmismatch_detection_animals)

        for mouse in rfid_detection_animals.keys():
            if mouse != None:
                if (rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] + rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection'] == 0):
                    about_rfid_detections[mouse] = {
                        'animalId': mouse,
                        'nbRFIDdetection': rfid_detection_animals[mouse]['nbRFIDdetection'],
                        'nbRFIDmatchdetection': rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'],
                        'nbRFIDmismatchdetection': rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection'],
                        'match_mismatch_proportion': [0, 0]
                    }
                    reliabilityContext.update(
                        {'rfidDetection': rfidDetection, 'about_rfid_detections': about_rfid_detections,
                         'rfid_detection_animals': rfid_detection_animals,
                         'rfidmatch_detection_animals': rfidmatch_detection_animals,
                         'rfidmismatch_detection_animals': rfidmismatch_detection_animals})
                else:
                    about_rfid_detections[mouse] = {
                        'animalId': mouse,
                        'nbRFIDdetection': rfid_detection_animals[mouse]['nbRFIDdetection'],
                        'nbRFIDmatchdetection': rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'],
                        'nbRFIDmismatchdetection': rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection'],
                        'match_mismatch_proportion': [rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] / (rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] + rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection']) * 100,
                rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection'] / (rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] + rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection']) * 100]
                    }
                reliabilityContext.update({'rfidDetection': rfidDetection, 'about_rfid_detections': about_rfid_detections,
                                           'rfid_detection_animals': rfid_detection_animals,
                                           'rfidmatch_detection_animals': rfidmatch_detection_animals,
                                           'rfidmismatch_detection_animals': rfidmismatch_detection_animals})
    else:
        about_rfid_detections = 'no rfid'
        reliabilityContext.update({'rfidDetection': rfidDetection, 'about_rfid_detections': about_rfid_detections})

    print(about_rfid_detections)

    #
    # rfid_detection_animals = infoFromFile['rfid_detection_animals']
    # rfidmatch_detection_animals = infoFromFile['rfidmatch_detection_animals']
    # rfidmismatch_detection_animals = infoFromFile['rfidmismatch_detection_animals']

    print('Sensors')
    # sensors
    if infoFromFile['sensors'] != "no sensors":
        timeline = infoFromFile['sensors']['timeline']
        temperature = infoFromFile['sensors']['temperature']
        humidity = infoFromFile['sensors']['humidity']
        sound = infoFromFile['sensors']['sound']
        lightvisible = infoFromFile['sensors']['lightvisible']
        lightvisibleandir = infoFromFile['sensors']['lightvisibleandir']
        highTemp = infoFromFile['sensors']['highTemp']
        lowTemp = infoFromFile['sensors']['lowTemp']
        if highTemp == False:
            highTempColor = "green"
            highTempIcon = "check icon"
            highTempInformation = "The temperature didn't exceed 25°C."
        elif highTemp == "high":
            highTempColor = "orange"
            highTempIcon = "sun icon"
            highTempInformation = "The temperature exceeded 25°C during the experiment but didn't reach 26°C."
        else:
            highTempColor = "red"
            highTempIcon = "hotjar icon"
            highTempInformation = "The temperature exceeded 26°C during the experiment."

        if lowTemp == False:
            lowTempColor = "green"
            lowTempIcon = "check icon"
            lowTempInformation = "The temperature wasn't lower than 21°C."
        elif lowTemp == "low":
            lowTempColor = "teal"
            lowTempIcon = "snowflake outline icon icon"
            lowTempInformation = "The temperature was below 21°C but was still above 20°C."
        else:
            lowTempColor = "blue"
            lowTempIcon = "igloo icon"
            lowTempInformation = "The temperature was below 21°C."

        sensors = {'sensors': "sensors", 'temperature': temperature,
                   'timeline': timeline, 'humidity': humidity, 'sound': sound, 'lightvisible': lightvisible,
                   'lightvisibleandir': lightvisibleandir, 'highTemp': highTemp, 'lowTemp': lowTemp,
                   'highTempColor': highTempColor, 'highTempIcon': highTempIcon,
                   'highTempInformation': highTempInformation,
                   'lowTempColor': lowTempColor, 'lowTempIcon': lowTempIcon, 'lowTempInformation': lowTempInformation}
    else:
        sensors = {'sensors': "no sensors"}

    reliabilityContext.update(sensors)
    progress_recorder.set_progress(10, 10, f'[Quality control] Reliability done')

    connection.close()
    print(file)
    # default_storage.delete(file


    instance = File.objects.get(id=file_id)
    # file_id = {'file_id': file_id}
    if deleteFile:
        print("Delete SQLite file")
        print('file id: ' + str(file_id))

        # url_deleteFile = 'http://127.0.0.1:8000/api/files/' + str(file_id['file_id'])
        # delete the file
        relative_url = reverse('files-detail', kwargs={'pk': str(file_id)})
        url_deleteFile = f"{settings.API_BASE_URL}{relative_url}"
        print(url_deleteFile)
        response = requests.delete(url_deleteFile)
        file_url = {'file_url': ''}

    else:
        try:
            # save the quality control into the database
            print('file id: ' + str(file_id))
            # url_deleteFile = 'http://127.0.0.1:8000/api/files/' + str(file_id['file_id'])
            relative_url = reverse('qualityControl')
            url_save_quality_control = f"{settings.API_BASE_URL}{relative_url}"
            # url_deleteFile = f"{settings.API_BASE_URL}{relative_url}"
            # # url_deleteFile = 'http://127.0.0.1:8000/api/files/' + str(file_id['file_id'])
            # print(url_deleteFile)
            response = requests.post(url_save_quality_control, {'file_id': file_id,
                                                                'quality_control': json.dumps(reliabilityContext)})
            print(response)
            print("[Task] Quality control saved")
            # file_url = {'file_url': ''}
            # file_url = {'file_url': MEDIA_URL+str(instance.sqlite)}
            # print(MEDIA_URL)
            # print('file_url: '+file_url['file_url'])
        except Exception as e:
            print(e)

    file_id = {'file_id': file_id}
    reliabilityContext.update(file_id)
    # reliabilityContext.update(file_url)
    return reliabilityContext


@shared_task(bind=True)
def activityPerTimeBin(self, file, time_bin=10):
    '''
    :param file: the SQLite LMT_v1_0_3 file
    :param time_bin: the time bin in minutes
    :return: activity per time_bin during the whole experiment
    '''
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 2, f'[Activity per timebin] Starting')

    # Extract activity
    progress_recorder.set_progress(1, 2, f'[Activity per timebin] Extracting activity for each animal')
    activity_per_time_bin = extractActivityPerAnimalWholeExperiment(file, time_bin)

    # save results in the LMT-toolkit database


    progress_recorder.set_progress(2, 2, f'[Activity per timebin] Job done: activity extracted')

    return activity_per_time_bin


@shared_task(bind=True)
def buildNightEventTask(self, file, startHour, endHour, version):
    '''
    :param file: the SQLite LMT_v1_0_3 file
    :param startHour: the start time of the night period in string like "19:00"
    :param endHour: the end time of the night period in string like "07:00"
    '''
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 1, f'[Nights rebuild] Starting')

    startTimeNight = datetime.time(hour=int(startHour.split(':')[0]), minute=int(startHour.split(':')[1]))
    endTimeNight = datetime.time(hour=int(endHour.split(':')[0]), minute=int(endHour.split(':')[1]))

    try:
        buildNightEvent(file, startTimeNight, endTimeNight, version)
        result = "success: night events rebuilt"
    except:
        result = "error during night rebuild"

    progress_recorder.set_progress(1, 1, f'[Nights rebuild] Job done: nights rebuilt')

    return result


