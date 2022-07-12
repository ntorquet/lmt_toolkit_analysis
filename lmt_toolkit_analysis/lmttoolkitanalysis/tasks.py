import os

from lmt_toolkit_analysis.celery import app
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from .methods import *
from .models import File
from datetime import date
import requests
import json
from lmttoolkitanalysis.methods import *
from lmt_toolkit_analysis.settings import MEDIA_ROOT






@shared_task(bind=True)
def getReliability(self, file, deleteFile = False, file_id = ""):

    '''
    :param file: the SQLite LMT file
    :return: extracted data
    '''
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 9, f'Starting')
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
    progress_recorder.set_progress(1, 9, f'File loaded')
    print(connection)
    print("gna2")
    # from .methods import findMiceInSQLiteFile

    mice = findMiceInSQLiteFile(connection)
    print("gna3")
    progress_recorder.set_progress(2, 9, f'Mice identified')
    # from .methods import findStartandEndInSQLiteFile
    startAndEnd = findStartandEndInSQLiteFile(connection)

    progress_recorder.set_progress(3, 9, f'Time information found')
    # from .methods import getSensorInSQLiteFile
    sensors = getSensorInSQLiteFile(connection)
    progress_recorder.set_progress(4, 9, f'Sensors information done')
    # from .methods import checkOmittedFrames
    omissions = checkOmittedFrames(connection)
    progress_recorder.set_progress(5, 9, f'Omissions calculated')
    # from .methods import getAnimalDetection
    list_detection_animals = getAnimalDetection(connection)
    progress_recorder.set_progress(6, 9, f'Animal detection done')
    # from .methods import checkAnimalDetectionOmissions
    percentageOfDetection = checkAnimalDetectionOmissions(omissions['theoricalNumberOfFrame'],
                                                          omissions['nbFramesRecorded'], list_detection_animals)
    # from .methods import getRFIDdetections
    rfid_detection_animals = getRFIDdetections(connection)
    progress_recorder.set_progress(7, 9, f'RFID detection loaded')
    # from .methods import getRFIDmatchDetections
    rfidmatch_detection_animals = getRFIDmatchDetections(connection)
    progress_recorder.set_progress(8, 9, f'RFID match done')
    # from .methods import getRFIDmismatchDetections
    rfidmismatch_detection_animals = getRFIDmismatchDetections(connection)
    progress_recorder.set_progress(9, 9, f'RFID mismatch done')

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

    print('glou')

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

    rfid_detection_animals = infoFromFile['rfid_detection_animals']
    rfidmatch_detection_animals = infoFromFile['rfidmatch_detection_animals']
    rfidmismatch_detection_animals = infoFromFile['rfidmismatch_detection_animals']

    print('glop')
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
                   'rfid_detection_animals': rfid_detection_animals,
                   'rfidmatch_detection_animals': rfidmatch_detection_animals,
                   'rfidmismatch_detection_animals': rfidmismatch_detection_animals
                   }
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

    # forms
    # mice_form1 = forms.formset_factory(addSubject, extra=0)
    # mice_form = mice_form1(initial=reliabilityContext['mouse'])
    # numberOfMice = len(mice_form)
    # # formice_form = zip(mice_form, reliabilityContext['mouse'])
    # formice_form = {'mice_form': mice_form, 'mouse': reliabilityContext['mouse']}

    # experiment_form = addExperiment()
    # experiment_form.fields['name_experiment'].initial = filename
    # experiment_form['xp_file_name'].initial = filename
    # group_form = addGroup()
    # protocol_form = addProtocol()
    # project_form = addProject()

    # all zip variables must be excluded from the data to be serialised and accessible for pdf creation
    # aboutDetections = zip(list_detection_animals, percentageOfDetection)
    # aboutDetections = {'list_detection_animals': list_detection_animals, 'percentageOfDetection': percentageOfDetection}
    # print(list_detection_animals)

    # about_rfid_detections = zip(list_rfid_detection_animals,
    #                             list_rfidmatch_detection_animals,
    #                             list_rfidmismatch_detection_animals)
    # about_rfid_detections = {'list_rfid_detection_animals': list_rfid_detection_animals, 'list_rfidmatch_detection_animals': list_rfidmatch_detection_animals, 'list_rfidmismatch_detection_animals': list_rfidmismatch_detection_animals}

    # rfid_detection_animals = infoFromFile['rfid_detection_animals']
    # rfidmatch_detection_animals = infoFromFile['rfidmatch_detection_animals']
    # rfidmismatch_detection_animals = infoFromFile['rfidmismatch_detection_animals']

    about_rfid_detections = {}
    for mouse in rfid_detection_animals.keys():
        about_rfid_detections[mouse] = {
            'animalId': mouse,
            'nbRFIDdetection': rfid_detection_animals[mouse]['nbRFIDdetection'],
            'nbRFIDmatchdetection': rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'],
            'nbRFIDmismatchdetection': rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection'],
            'match_mismatch_proportion': [rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] / (rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] + rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection']) * 100,
    rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection'] / (rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] + rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection']) * 100]
        }

    if len(rfid_detection_animals) > 0:
        rfidDetection = True
    else:
        rfidDetection = False

    # match_mismatch_proportion = []
    # for i, j in zip(list_rfidmatch_detection_animals,
    #                 list_rfidmismatch_detection_animals):
    #     currentAnimal = [
    #         i['nbRFIDmatchdetection'] / (i['nbRFIDmatchdetection'] + j['nbRFIDmismatchdetection']) * 100,
    #         j['nbRFIDmismatchdetection'] / (
    #                 i['nbRFIDmatchdetection'] + j['nbRFIDmismatchdetection']) * 100]
    #     match_mismatch_proportion.append(currentAnimal)

    context = {#'group_form': group_form, 'project_form': project_form, 'protocol_form': protocol_form,
               # 'formice_form': formice_form,
               'numberOfMice': numberOfMice,# 'experiment_form': experiment_form,
               'aboutDetections': aboutDetections,
                'list_detection_animals': list_detection_animals, 'percentageOfDetection': percentageOfDetection,
                'rfid_detection_animals': rfid_detection_animals,
                'rfidmatch_detection_animals': rfidmatch_detection_animals,
                'rfidmismatch_detection_animals': rfidmismatch_detection_animals,
                'about_rfid_detections': about_rfid_detections, 'rfidDetection': rfidDetection
               # 'match_mismatch_proportion': match_mismatch_proportion
            }
    reliabilityContext.update(context)
    print("hips")
    # Remove the file from the temp folder

    connection.close()
    print(file)
    # default_storage.delete(file)

    print("oupsi")

    # deleteFile
    if deleteFile:
        print("Delete SQLite file")
        print('file id: '+str(file_id))
        instance = File.objects.get(id=file_id)
        if instance.sqlite:
            os.remove(os.path.join(MEDIA_ROOT, str(instance.sqlite)))
        # instance.delete()

    return reliabilityContext

