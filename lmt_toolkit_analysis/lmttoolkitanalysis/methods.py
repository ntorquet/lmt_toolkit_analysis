'''
Created by Nicolas Torquet at 23/09/2020
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
'''


import sqlite3
import datetime
from math import *
from sqlite3 import Error

from .LMT_v1_0_5b.lmtanalysis.Animal import *
from .LMT_v1_0_5b.lmtanalysis.EventTimeLineCache import EventTimeLineCached
from .LMT_v1_0_5b.lmtanalysis.FileUtil import behaviouralEventOneMouse
from .LMT_v1_0_5b.scripts.ComputeMeasuresIdentityProfileOneMouseAutomatic import computeProfile
from .LMT_v1_0_5b.scripts.Rebuild_info_animals import addColumns, updateField

oneFrame = 1
oneSecond = 30
oneMinute = 30*60
oneHour = 30*60*60
oneDay = 30*60*60*24
oneWeek = 30*60*60*24*7


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    print('################################################################################################')
    print('Connection')
    print(type(db_file))
    print(db_file)
    # db_file = r'C:/Users/torquetn/Documents/F_21_WT_26_Experiment 3425.sqlite'
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print('Error '+e)

    return conn

def findMiceInSQLiteFile(connection):
    '''
    :param LMTFile: the SQLite LMT_v1_0_3 file
    :return: animals in a list of dico
    '''
    cursor = connection.cursor()
    query = "SELECT * FROM ANIMAL"
    cursor.execute(query)
    columnNames = [description[0] for description in cursor.description]
    print("Into findMiceInSQLiteFile")

    list_animals = []
    rows = cursor.fetchall()
    for row in rows:
        for i in range(0, len(row)):
            list_animals.append({columnNames[i]: row[i]})
        # animalId = row[0]
        # rfid = row[1]
        # genotype = row[2]
        # name = row[3]
        # list_animals.append({'animalId': animalId, 'tag_subject': rfid, 'genotype': genotype, 'name_subject': name})
    cursor.close()
    print(str(columnNames))
    print(str(list_animals))
    return list_animals


def findStartandEndInSQLiteFile(connection):
    '''
    :param connection: the SQLite LMT_v1_0_3 file
    :return: the start and the end of the experiment
    '''

    cursor = connection.cursor()
    query = "SELECT min(TIMESTAMP), max(TIMESTAMP) FROM FRAME"

    cursor.execute(query)

    rows = cursor.fetchall()
    for row in rows:
        startDate = datetime.datetime.fromtimestamp(row[0] / 1000).strftime("%Y-%m-%d %H:%M:%S")
        endDate = datetime.datetime.fromtimestamp(row[1] / 1000).strftime("%Y-%m-%d %H:%M:%S")
        realStartInSeconds = row[0]/1000
        realEndInSeconds = row[1] / 1000
        experienceDates = {'start_experiment': startDate, 'end_experiment': endDate, 'realStartInSeconds': realStartInSeconds, 'realEndInSeconds': realEndInSeconds}
    cursor.close()
    return experienceDates


def getSensorInSQLiteFile(connection):
    '''
    :param connection: the SQLite LMT_v1_0_3 file
    :return: the temperature recorded during the whole experiment, with timestamp
    '''
    cursor = connection.cursor()

    try:
        queryNumber = "SELECT COUNT(TEMPERATURE) FROM FRAME"
        cursor.execute(queryNumber)
        numberOfRows = cursor.fetchone()

        # flag to report high or low tempertaure during the experiment
        highTemp = False
        lowTemp = False
        queryVeryHighTemp = "SELECT TEMPERATURE FROM FRAME WHERE TEMPERATURE > 26"
        cursor.execute(queryVeryHighTemp)
        if len(cursor.fetchall()) > 0:
            highTemp = "veryHigh"
        else:
            queryHighTemp = "SELECT TEMPERATURE FROM FRAME WHERE TEMPERATURE > 25"
            cursor.execute(queryHighTemp)
            if len(cursor.fetchall()) > 0:
                highTemp = "high"

        queryVeryLowTemp = "SELECT TEMPERATURE FROM FRAME WHERE TEMPERATURE < 20"
        cursor.execute(queryVeryLowTemp)
        if len(cursor.fetchall()) > 0:
            lowTemp = "veryLow"
        else:
            queryLowTemp = "SELECT TEMPERATURE FROM FRAME WHERE TEMPERATURE < 21"
            cursor.execute(queryLowTemp)
            if len(cursor.fetchall()) > 0:
                lowTemp = "low"


        query = "SELECT TIMESTAMP, TEMPERATURE, HUMIDITY, SOUND, LIGHTVISIBLE, LIGHTVISIBLEANDIR FROM FRAME ORDER BY FRAMENUMBER"
        cursor.execute(query)
        rows = cursor.fetchall()
        timeline = []
        temperature = []
        humidity = []
        sound = []
        lightvisible = []
        lightvisibleandir = []
        for row in rows:
            timeline.append(datetime.datetime.fromtimestamp(row[0] / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
            temperature.append(row[1])
            humidity.append(row[2])
            sound.append(row[3])
            lightvisible.append(row[4])
            lightvisibleandir.append(row[5])
        cursor.close()

        timelineToReturn = []
        temperatureToReturn = []
        humidityToReturn = []
        soundToReturn = []
        lightvisibleToReturn = []
        lightvisibleandirToReturn = []
        # step to have 200 dots, what ever the number of frame
        if numberOfRows[0] < 200:
            step = 1
        else:
            step = round(numberOfRows[0] / 200)
        for i in range(0, numberOfRows[0], step):
            timelineToReturn.append(timeline[i])
            temperatureToReturn.append(temperature[i])
            humidityToReturn.append(humidity[i])
            soundToReturn.append(sound[i])
            lightvisibleToReturn.append(lightvisible[i])
            lightvisibleandirToReturn.append(lightvisibleandir[i])
        result = {'timeline': timelineToReturn, 'temperature': temperatureToReturn, 'humidity': humidityToReturn, 'sound': soundToReturn,
                  'lightvisible': lightvisibleToReturn, 'lightvisibleandir': lightvisibleandirToReturn, 'highTemp': highTemp, 'lowTemp': lowTemp}
        return result

    except:
        return "no sensors"

def checkOmittedFrames(connection):
    '''
    :param connection: the SQLite LMT_v1_0_3 file
    :return: Number of omitted frames
    '''

    startAndEnd = findStartandEndInSQLiteFile(connection)
    startXp = startAndEnd['start_experiment']
    endXp = startAndEnd['end_experiment']
    realStartInSeconds = startAndEnd['realStartInSeconds']
    realEndInSeconds = startAndEnd['realEndInSeconds']
    realDurationInSeconds = realEndInSeconds - realStartInSeconds + 1
    realDurationInMinutes = realDurationInSeconds / 60
    realDurationInHours = realDurationInMinutes /60
    realDurationInDays = realDurationInHours / 24
    theoricalNumberOfFrame = realDurationInSeconds * 30 #30 fps

    c = connection.cursor()

    query = "SELECT * FROM FRAME"
    c.execute(query)
    framesRecorded = c.fetchall()
    nbFramesRecorded = len(framesRecorded)
    nbFramesRecordedInSeconds = nbFramesRecorded / oneSecond
    nbFramesRecordedInMinutes = nbFramesRecorded / oneMinute
    nbFramesRecordedInHours = nbFramesRecorded / oneHour
    nbFramesRecordedInDays = nbFramesRecorded / oneDay

    query = "SELECT MIN(FRAMENUMBER) FROM FRAME"
    c.execute(query)
    minFrames = c.fetchall()
    for minFrame in minFrames:
        startFrame = minFrame[0]

    query = "SELECT MAX(FRAMENUMBER) FROM FRAME"
    c.execute(query)
    maxFrames = c.fetchall()
    for maxFrame in maxFrames:
        endFrame = maxFrame[0]

    durationExpFromFrame = endFrame - startFrame + 1
    nbOmittedFrames = ceil(realDurationInSeconds * oneSecond - nbFramesRecorded)
    percentageOfOmittedFrames = round(100 * nbOmittedFrames / (realDurationInSeconds * oneSecond), 6)
    c.close()

    nbOmittedSeconds = realDurationInSeconds - nbFramesRecordedInSeconds
    nbOmittedMinutes = realDurationInMinutes - nbFramesRecordedInMinutes
    nbOmittedHours = realDurationInHours - nbFramesRecordedInHours
    nbOmittedDays = realDurationInDays - nbFramesRecordedInDays

    realDurationInSeconds = round(realDurationInSeconds, 2)
    realDurationInMinutes = round(realDurationInMinutes, 2)
    realDurationInHours = round(realDurationInHours, 2)
    realDurationInDays = round(realDurationInDays, 2)
    nbFramesRecordedInSeconds = round(nbFramesRecordedInSeconds, 2)
    nbFramesRecordedInMinutes = round(nbFramesRecordedInMinutes, 2)
    nbFramesRecordedInHours = round(nbFramesRecordedInHours, 2)
    nbFramesRecordedInDays = round(realDurationInDays, 2)
    nbOmittedSeconds = round(nbOmittedSeconds, 4)
    nbOmittedMinutes = round(nbOmittedMinutes, 6)
    nbOmittedHours = round(nbOmittedHours, 8)
    nbOmittedDays = round(nbOmittedDays, 10)

    result = {'realDurationInSeconds': realDurationInSeconds, 'realDurationInMinutes':realDurationInMinutes, 'realDurationInHours': realDurationInHours,
              'realDurationInDays': realDurationInDays, 'theoricalNumberOfFrame': theoricalNumberOfFrame, 'nbFramesRecorded': nbFramesRecorded,
              'nbFramesRecordedInSeconds': nbFramesRecordedInSeconds, 'nbFramesRecordedInMinutes': nbFramesRecordedInMinutes,
              'nbFramesRecordedInHours': nbFramesRecordedInHours, 'nbFramesRecordedInDays': nbFramesRecordedInDays,
              'durationExpFromFrame': durationExpFromFrame, 'nbOmittedFrames': nbOmittedFrames, 'percentageOfOmittedFrames': percentageOfOmittedFrames,
              'nbOmittedSeconds': nbOmittedSeconds, 'nbOmittedMinutes': nbOmittedMinutes, 'nbOmittedHours': nbOmittedHours, 'nbOmittedDays': nbOmittedDays}
    return result



def getAnimalDetection(connection):
    '''
    :param connection: the SQLite LMT_v1_0_3 file
    :return: number of detection per animal during the whole experiment
    '''
    c = connection.cursor()

    query = "SELECT ANIMALID, COUNT(*) FROM DETECTION GROUP BY ANIMALID"
    c.execute(query)

    rows = c.fetchall()
    list_detection_animals = []
    for row in rows:
        animalId = row[0]
        nbDetection = row[1]
        list_detection_animals.append({'animalId': animalId, 'nbDetection': nbDetection})

    c.close()

    return list_detection_animals


def checkAnimalDetectionOmissions(theoricalNumberOfFrame, nbFramesRecorded, list_detection_animals):
    '''
    :param theoricalNumberOfFrame: from checkOmittedFrames()
    :param nbFramesRecorded:  from checkOmittedFrames()
    :param list_detection_animals: from getAnimalDetection()
    :return: dico with percentage of frames where each animal was detected
    '''
    listPercentageOfDetection = []

    for row in list_detection_animals:
        alert = False
        animalId = row['animalId']
        detectionPercentTheoricalFrames = round(row['nbDetection']/theoricalNumberOfFrame*100, 2)
        detectionPercentRecordedFrames = round(row['nbDetection']/nbFramesRecorded*100,2)
        if animalId is None:
            if detectionPercentTheoricalFrames > 50:
                detectionPercentTheoricalFramesColor = "red"
                alert = True
            else:
                detectionPercentTheoricalFramesColor = "green"

            if detectionPercentRecordedFrames > 50:
                detectionPercentRecordedFramesColor = "red"
                alert = True
            else:
                detectionPercentRecordedFramesColor = "green"

            if alert:
                messageDetectionFrameColor = "red"
                messageDetectionFrame = "Detected individuals were unidentified in more than 50% of the frames."
                messageDetectionFramesIcon = "hotjar icon"
            else:
                messageDetectionFrameColor = "green"
                messageDetectionFrame = "Frames with unidentified individuals represent less than 50% of the total number of frames."
                messageDetectionFramesIcon = "check icon"
        else:
            if detectionPercentTheoricalFrames < 50:
                detectionPercentTheoricalFramesColor = "red"
                alert = True
            else:
                detectionPercentTheoricalFramesColor = "green"

            if detectionPercentRecordedFrames < 50:
                detectionPercentRecordedFramesColor = "red"
                alert = True
            else:
                detectionPercentRecordedFramesColor = "green"

            if alert:
                messageDetectionFrameColor = "red"
                messageDetectionFrame = "This animal was identified in less than 50% of the frames."
                messageDetectionFramesIcon = "hotjar icon"
            else:
                messageDetectionFrameColor = "green"
                messageDetectionFrame = "This animal was identified in more than 50% of the frames."
                messageDetectionFramesIcon = "check icon"

        listPercentageOfDetection.append({'animalId': animalId, 'detectionPercentTheoricalFrames': detectionPercentTheoricalFrames,
                                          'detectionPercentRecordedFrames': detectionPercentRecordedFrames,
                                          'detectionPercentTheoricalFramesColor': detectionPercentTheoricalFramesColor,
                                          'detectionPercentRecordedFramesColor': detectionPercentRecordedFramesColor,
                                          'messageDetectionFrameColor': messageDetectionFrameColor,
                                          'messageDetectionFramesIcon': messageDetectionFramesIcon, 'messageDetectionFrame': messageDetectionFrame
                                          })
    return listPercentageOfDetection


def getRFIDdetections(connection):
    '''
    :param connection: the SQLite LMT_v1_0_3 file
    :return: number of RFID detection for each animal
    '''
    list_animals = findMiceInSQLiteFile(connection)

    c = connection.cursor()

    query = "SELECT IDANIMALA, COUNT(STARTFRAME) FROM EVENT WHERE NAME LIKE 'RFID%' GROUP BY IDANIMALA"
    c.execute(query)

    rows = c.fetchall()
    list_rfid_detection_animals = []
    rfid_detection_animals = {}
    for row in rows:
        animalId = row[0]
        nbRFIDdetection = row[1]
        list_rfid_detection_animals.append({'animalId': animalId, 'nbRFIDdetection': nbRFIDdetection})
        rfid_detection_animals[animalId] = {'nbRFIDdetection': nbRFIDdetection}

    c.close()

    for animal in list_animals:
        print('animalID: '+str(animal['ID']))
        if not animal['ID'] in rfid_detection_animals.keys():
            rfid_detection_animals[animal['ID']] = {'nbRFIDdetection': 0}
            # if not 'RFID' in animal['tag_subject']:
            #     rfid_detection_animals[animal['animalId']] = {'nbRFIDdetection': 0}
            # else:
            #     rfid_detection_animals[animal['animalId']] = {'nbRFIDdetection': nan}

    # return list_rfid_detection_animals
    return rfid_detection_animals


def getRFIDmatchDetections(connection):
    '''
    :param connection: the SQLite LMT_v1_0_3 file
    :return: number of RFID match detection for each animal
    '''
    list_animals = findMiceInSQLiteFile(connection)

    c = connection.cursor()

    query = "SELECT IDANIMALA, COUNT(*) FROM EVENT WHERE NAME = 'RFID MATCH' GROUP BY IDANIMALA "
    c.execute(query)

    rows = c.fetchall()
    list_rfidmatch_detection_animals = []
    rfidmatch_detection_animals = {}
    for row in rows:
        animalId = row[0]
        nbRFIDmatchdetection = row[1]
        list_rfidmatch_detection_animals.append({'animalId': animalId, 'nbRFIDmatchdetection': nbRFIDmatchdetection})
        rfidmatch_detection_animals[animalId]= {'nbRFIDmatchdetection': nbRFIDmatchdetection}

    c.close()

    for animal in list_animals:
        if not animal['animalId'] in rfidmatch_detection_animals.keys():
            rfidmatch_detection_animals[animal['animalId']] = {'nbRFIDmatchdetection': 0}
            # if not 'RFID' in animal['tag_subject']:
            #     rfidmatch_detection_animals[animal['animalId']] = {'nbRFIDmatchdetection': 0}
            # else:
            #     rfidmatch_detection_animals[animal['animalId']] = {'nbRFIDmatchdetection': nan}


    # return list_rfidmatch_detection_animals
    return rfidmatch_detection_animals


def getRFIDmismatchDetections(connection):
    '''
    :param connection: the SQLite LMT_v1_0_3 file
    :return: number of RFID mismatch detection for each animal
    '''
    list_animals = findMiceInSQLiteFile(connection)

    c = connection.cursor()

    query = "SELECT IDANIMALA, COUNT(*) FROM EVENT WHERE NAME = 'RFID MISMATCH' GROUP BY IDANIMALA "
    c.execute(query)

    rows = c.fetchall()
    list_rfidmismatch_detection_animals = []
    rfidmismatch_detection_animals = {}
    for row in rows:
        animalId = row[0]
        nbRFIDmismatchdetection = row[1]
        list_rfidmismatch_detection_animals.append({'animalId': animalId, 'nbRFIDmismatchdetection': nbRFIDmismatchdetection})
        rfidmismatch_detection_animals[animalId] = {'nbRFIDmismatchdetection': nbRFIDmismatchdetection}

    c.close()

    for animal in list_animals:
        if not animal['animalId'] in rfidmismatch_detection_animals.keys():
            rfidmismatch_detection_animals[animal['animalId']] = {'nbRFIDmismatchdetection': 0}
            # if not 'RFID' in animal['tag_subject']:
            #     rfidmismatch_detection_animals[animal['animalId']] = {'nbRFIDmismatchdetection': 0}
            # else:
            #     rfidmismatch_detection_animals[animal['animalId']] = {'nbRFIDmismatchdetection': nan}

    # return list_rfidmismatch_detection_animals
    return rfidmismatch_detection_animals





def getInformationsFromSQLite(LMTFile):
    file = LMTFile
    connection = sqlite3.connect(file)

    mice = findMiceInSQLiteFile(connection)
    startAndEnd = findStartandEndInSQLiteFile(connection)
    sensors = getSensorInSQLiteFile(connection)
    omissions = checkOmittedFrames(connection)
    list_detection_animals = getAnimalDetection(connection)
    percentageOfDetection = checkAnimalDetectionOmissions(omissions['theoricalNumberOfFrame'],
                                                          omissions['nbFramesRecorded'], list_detection_animals)
    # list_rfid_detection_animals = getRFIDdetections(connection)
    # list_rfidmatch_detection_animals = getRFIDmatchDetections(connection)
    # list_rfidmismatch_detection_animals = getRFIDmismatchDetections(connection)

    rfid_detection_animals = getRFIDdetections(connection)
    rfidmatch_detection_animals = getRFIDmatchDetections(connection)
    rfidmismatch_detection_animals = getRFIDmismatchDetections(connection)

    dicoInfo = {'mice': mice, 'startAndEnd': startAndEnd, 'sensors': sensors, 'omissions': omissions, 'list_detection_animals': list_detection_animals,
                'rfid_detection_animals': rfid_detection_animals, 'rfidmatch_detection_animals': rfidmatch_detection_animals,
                'rfidmismatch_detection_animals': rfidmismatch_detection_animals,
                'percentageOfDetection': percentageOfDetection}

    connection.close()
    return dicoInfo


def getReliability(file):
    '''
    :param file: the SQLite LMT_v1_0_3 file
    :return: extracted data
    '''
    print("In getReliability")

    infoFromFile = getInformationsFromSQLite(file)
    mice = infoFromFile['mice']
    xpDates = infoFromFile['startAndEnd']
    startXp = xpDates['start_experiment']
    endXp = xpDates['end_experiment']
    # print(mice)

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
    nbOmittedHours = infoFromFile['omissions']['nbOmitedHours']
    nbOmittedDays = infoFromFile['omissions']['nbOmittedDays']
    # message depending of percentage of omissions
    if percentageOfOmittedFrames < 0:
        omissionColor = "red"
        omissionIcon = "times icon"
        omissionInformation = "There are more recorded frames than expected: there is a problem with the acquisition. This file should not be used."
    elif percentageOfOmittedFrames < 0.08:
        omissionColor = "green"
        omissionIcon = "check icon"
        omissionInformation = "The number of dropped frames is limited."
    elif percentageOfOmittedFrames < 1:
        omissionColor = "orange"
        omissionIcon = "exclamation icon"
        omissionInformation = "The number of dropped frames is acceptable."
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


    reliabilityContext = {'mouse': mice, 'xpDates': xpDates,
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
                   'omissionInformation': omissionInformation, 'list_detection_animals': list_detection_animals,
                   'percentageOfDetection': percentageOfDetection,
                   'aboutDetections': aboutDetections
    }

    # list_rfid_detection_animals = infoFromFile['list_rfid_detection_animals']
    # list_rfidmatch_detection_animals = infoFromFile['list_rfidmatch_detection_animals']
    # list_rfidmismatch_detection_animals = infoFromFile['list_rfidmismatch_detection_animals']

    rfidDetection = False
    about_rfid_detections = {}
    for mouse in mice:
        if not 'RFID' in mouse['tag_subject']:
            rfidDetection = True

    if rfidDetection:
        rfid_detection_animals = infoFromFile['rfid_detection_animals']
        rfidmatch_detection_animals = infoFromFile['rfidmatch_detection_animals']
        rfidmismatch_detection_animals = infoFromFile['rfidmismatch_detection_animals']
        # print(rfid_detection_animals)
        # print(rfidmatch_detection_animals)
        # print(rfidmismatch_detection_animals)

        for mouse in rfid_detection_animals.keys():
            about_rfid_detections[mouse] = {
                'animalId': mouse,
                'nbRFIDdetection': rfid_detection_animals[mouse]['nbRFIDdetection'],
                'nbRFIDmatchdetection': rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'],
                'nbRFIDmismatchdetection': rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection'],
                'match_mismatch_proportion': [rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] / (rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] + rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection']) * 100,
        rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection'] / (rfidmatch_detection_animals[mouse]['nbRFIDmatchdetection'] + rfidmismatch_detection_animals[mouse]['nbRFIDmismatchdetection']) * 100]
            }
    else:
        about_rfid_detections = 'no rfid'

    print(about_rfid_detections)
    reliabilityContext.update({'rfidDetection': rfidDetection, 'about_rfid_detections': about_rfid_detections})


    # if len(rfid_detection_animals) > 0:
    #     rfidDetection = True
    # else:
    #     rfidDetection = False



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

        sensors = {'temperature': temperature,
                   'timeline': timeline, 'humidity': humidity, 'sound': sound, 'lightvisible': lightvisible,
                   'lightvisibleandir': lightvisibleandir, 'highTemp': highTemp, 'lowTemp': lowTemp,
                   'highTempColor': highTempColor, 'highTempIcon': highTempIcon, 'highTempInformation': highTempInformation,
                   'lowTempColor': lowTempColor, 'lowTempIcon': lowTempIcon, 'lowTempInformation': lowTempInformation}
    else:
        sensors = {'sensors': "no sensors"}

    reliabilityContext.update(sensors)

    return reliabilityContext


################## Analysis ##################

def getStartEndExperiment(connection):
    c = connection.cursor()
    query = "SELECT MIN(FRAMENUMBER), MAX(FRAMENUMBER) FROM FRAME"
    c.execute(query)
    StartEndFrames = c.fetchall()
    for row in StartEndFrames:
        # print(str(row))
        startFrame = row[0]
        endFrame = row[1]

    return [startFrame, endFrame]




def getDistanceAndTimeInContact(connection, minT, maxT, file):
    # load animal pool
    pool = AnimalPool()
    pool.loadAnimals(connection)

    dataDic = {}
    for animal in pool.animalDictionnary.keys():
        # store the info about the animal
        print("computing individual animal: {}".format(animal))
        animalObject = pool.animalDictionnary[animal]
        rfid = animalObject.RFID
        print("RFID: {}".format(rfid))
        dataDic[rfid] = {}
        dataDic[rfid]["animal"] = animalObject.name
        dataDic[rfid]["file"] = file
        dataDic[rfid]['genotype'] = animalObject.genotype
        dataDic[rfid]['sex'] = animalObject.sex
        dataDic[rfid]['strain'] = animalObject.strain
        dataDic[rfid]['age'] = animalObject.age

        # compute distance traveled during the experiment (in m)
        animalObject.loadDetection(start=minT, end=maxT, lightLoad=True)
        dataDic[rfid]["totalDistance"] = animalObject.getDistance(tmin=minT, tmax=maxT) / 100

        # compute the time spent in contact during the experiment (in s)
        behavEvent = 'Contact'
        print("computing individual event: {}".format(behavEvent))

        behavEventTimeLine = EventTimeLineCached(connection, file, behavEvent, animal, minFrame=minT, maxFrame=maxT)
        # clean the behavioural event timeline from too close and too short events:
        behavEventTimeLine.mergeCloseEvents(numberOfFrameBetweenEvent=1)
        behavEventTimeLine.removeEventsBelowLength(maxLen=3)

        # compute duration, number and mean duration of contact events
        totalEventDuration = behavEventTimeLine.getTotalLength() / 30  # conversion in seconds
        nbEvent = behavEventTimeLine.getNumberOfEvent(minFrame=minT, maxFrame=maxT)
        print("total event duration: ", totalEventDuration)
        dataDic[rfid][behavEvent + " TotalLen"] = totalEventDuration
        dataDic[rfid][behavEvent + " Nb"] = nbEvent
        if nbEvent == 0:
            meanDur = 0
        else:
            meanDur = totalEventDuration / nbEvent
        dataDic[rfid][behavEvent + " MeanDur"] = meanDur  # in seconds

    # print to check the results
    print('data extracted from file: ', file)
    for rfid in dataDic.keys():
        print(
            '{} ({}) travelled {} m and spent {} s in contact with others ({} contact events of mean duration {} s)'.format(
                rfid, dataDic[rfid]['genotype'], dataDic[rfid]['totalDistance'], dataDic[rfid]['Contact TotalLen'],
                dataDic[rfid]['Contact Nb'], dataDic[rfid]['Contact MeanDur']))

    print('Job done.')

    return dataDic

def getDataProfile(connection, minT, maxT, file):
    animalPool = AnimalPool()
    #
    # # load infos about the animals
    animalPool.loadAnimals(connection)

    # head, tail = os.path.split(file)
    # extension = head[-4:]
    # print('extension: ', extension)
    profileData = {}
    profileData[file] = {}

    # text_file = getFileNameInput()
    # text_file_name = 'extra_'+file.split('\\')[2].split('.')[0]+".txt"
    # text_file = open ( text_file_name, "w")
    # # text_file = 'extra_'+file.split('\\')[2].split('.')[0]
    # print('text file extra: '+text_file_name)
    n = 0   # n=0 take all the nights
    # Compute profile2 data and save them in a text file
    profileData = computeProfile(file=file, minT=minT, maxT=maxT,  behaviouralEventList=behaviouralEventOneMouse)
    # Duration in frames: change to seconds
    for mouse in profileData:
        for key in profileData[mouse].keys():
            if 'TotalLen' in key or 'MeanDur' in key:
                profileData[mouse][key] = profileData[mouse][key]/30
        profileData[mouse]['Start frame'] = minT
        profileData[mouse]['End frame'] = maxT
        profileData[mouse]['Period of analysis'] = 'From start frame to end frame'

    return profileData


def saveAnimalInfo(file, dataJson):
    addColumns(file)
    formatedJson = {}
    for line in dataJson:
        formatedJson[line['tag_subject']] = {}
        for key, value in line.items():
            formatedJson[line['tag_subject']][key] = value

    updateField(file, formatedJson)