'''
Created by Nicolas Torquet at 12/07/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
'''

import os

from lmt_toolkit_analysis.celery import app
from celery import shared_task
from celery_progress.backend import ProgressRecorder

# from .LMT_v1_0_3.lmtanalysis.FileUtil import behaviouralEventOneMouse
# from .LMT_v1_0_3.scripts.ComputeMeasuresIdentityProfileOneMouseAutomatic import computeProfile, computeProfileWithoutText_file
from .LMT_v1_0_5b.scripts.Rebuild_All_Events import process
from .LMT_v1_0_5b.lmtanalysis.TaskLogger import TaskLogger
from .methods import *
from .models import File
from datetime import date
import requests
import json
from lmttoolkitanalysis.methods import *
from lmt_toolkit_analysis.settings import MEDIA_ROOT, MEDIA_URL

# import to analyse LMT_v1_0_3 data
import sqlite3
from .LMT_v1_0_5b.lmtanalysis.Animal import *
from .LMT_v1_0_5b.lmtanalysis.EventTimeLineCache import EventTimeLineCached



timeUnit = {
    'frame(s)': 1,
    'second(s)': 30,
    'minute(s)': 30*60,
    'hour(s)': 30*60*60,
    'day(s)': 30*60*60*24,
    'week(s)': 30*60*60*24*7,
}



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
        url_deleteFile = 'http://127.0.0.1:8000/api/v1/files/' + str(file_id['file_id'])
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
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 4, f'Starting')

    connection = create_connection(file)
    print('File: '+file)

    progress_recorder.set_progress(1, 4, f'File loaded')
    print(connection)

    StartEndFrames = getStartEndExperiment(connection)
    minT = StartEndFrames[0]
    maxT = StartEndFrames[1]

    connection.close()

    # Rebuild_all_event from minT to maxT
    progress_recorder.set_progress(3, 4, f'first analysis done - start Rebuild_all_event')
    process(file, minT, maxT)

    connection = create_connection(file)
    t = TaskLogger(connection)
    t.addLog("Rebuild all events", version=version)
    connection.close()

    # update file in database: rebuild field with version number
    api_url = f"http://127.0.0.1:8000/api/v1/files/{file_id}/"
    todo = {"rebuild": version}
    response = requests.patch(api_url, json=todo)
    # print(response.json())
    print(response.status_code)
    progress_recorder.set_progress(4, 4, f'Rebuild done - compute analysis')

    return {"message": "Rebuild done"}


@shared_task(bind=True)
def saveAnimalInfoTask(self, data):
    '''
    :param data: contains the SQLite LMT_v1_0_3 file and the info to save
    :return: job done
    '''
    print("in saveAnimalInfoTask")
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 4, f'Starting')
    file = data['file']
    animalsInfo = data ['animalsInfo']
    version = data['version']
    print(version)


    print('File: '+file)
    progress_recorder.set_progress(1, 4, f'File loaded')

    saveAnimalInfo(file, animalsInfo, version)

    progress_recorder.set_progress(3, 4, f'writing into the database')



    progress_recorder.set_progress(4, 4, f'Saving done')

    return {"message": "Saving done"}


@shared_task(bind=True)
def analyseProfileFromStartTimeToEndTime(self, file,  tmin = 0, tmax = -1, unitMinT = None, unitMaxT = None):
    '''
    :param file: the SQLite LMT_v1_0_3 file, tmin and tmax and their units (unitMinT and unitMaxT) as start and end for the analysis
    :return: profile (results of behaviors) for each animal
    '''

    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 2, f'Starting')

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

    progress_recorder.set_progress(1, 2, f'Start and end frames found')

    profileData = getDataProfile(connection, minT, maxT, file)
    # print("tmin: " + str(tmin))
    # print("unitMinT: "+str(unitMinT))
    # print("tmax: " + str(tmax))
    # print("unitMaxT: "+str(unitMaxT))
    # print("minT: "+str(minT))
    # print("maxT: "+str(maxT))

    progress_recorder.set_progress(2, 2, f'Analysis done')

    connection.close()

    return profileData


@shared_task(bind=True)
def getReliability(self, file, deleteFile = True, file_id = ""):
    '''
    :param file: the SQLite LMT_v1_0_3 file
    :return: reliability
    '''
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 10, f'Starting')

    connection = create_connection(file)
    print('File: '+file)
    progress_recorder.set_progress(1, 10, f'File loaded')
    print(connection)
    # from .methods import findMiceInSQLiteFile

    mice = findMiceInSQLiteFile(connection)
    progress_recorder.set_progress(2, 10, f'Mice identified')
    # from .methods import findStartandEndInSQLiteFile
    startAndEnd = findStartandEndInSQLiteFile(connection)

    progress_recorder.set_progress(3, 10, f'Time information found')
    # from .methods import getSensorInSQLiteFile
    sensors = getSensorInSQLiteFile(connection)
    progress_recorder.set_progress(4, 10, f'Sensors information done')
    # from .methods import checkOmittedFrames
    omissions = checkOmittedFrames(connection)
    progress_recorder.set_progress(5, 10, f'Omissions calculated')
    # from .methods import getAnimalDetection
    list_detection_animals = getAnimalDetection(connection)
    progress_recorder.set_progress(6, 10, f'Animal detection done')
    # from .methods import checkAnimalDetectionOmissions
    percentageOfDetection = checkAnimalDetectionOmissions(omissions['theoricalNumberOfFrame'],
                                                          omissions['nbFramesRecorded'], list_detection_animals)
    # from .methods import getRFIDdetections
    rfid_detection_animals = getRFIDdetections(connection)
    progress_recorder.set_progress(7, 10, f'RFID detection loaded')
    # from .methods import getRFIDmatchDetections
    rfidmatch_detection_animals = getRFIDmatchDetections(connection)
    progress_recorder.set_progress(8, 10, f'RFID match done')
    # from .methods import getRFIDmismatchDetections
    rfidmismatch_detection_animals = getRFIDmismatchDetections(connection)
    progress_recorder.set_progress(9, 10, f'RFID mismatch done')

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
    progress_recorder.set_progress(10, 10, f'Reliability done')

    connection.close()
    print(file)
    # default_storage.delete(file


    instance = File.objects.get(id=file_id)
    file_id = {'file_id': file_id}
    if deleteFile:
        print("Delete SQLite file")
        print('file id: ' + str(file_id))
        url_deleteFile = 'http://127.0.0.1:8000/api/v1/files/' + str(file_id['file_id'])
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

