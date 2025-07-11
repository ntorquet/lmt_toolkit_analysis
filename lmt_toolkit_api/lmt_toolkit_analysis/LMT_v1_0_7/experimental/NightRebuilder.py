'''
Created by Nicolas Torquet at 24/06/2025
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
'''

'''
This script manage the rebuild of night event.
There is several ways to do this:
1. from sensors: the data have to be verified by the user
2. from start hour and end hour of the night: user has to provide those information
3. from start hour and for a duration: user has to provide those information
'''



import sqlite3
from ..experimental.Animal_LMTtoolkit import *
from ..lmtanalysis.Event import *
from ..lmtanalysis.TaskLogger import TaskLogger
from ..lmtanalysis.Util import getStartInDatetime, getEndInDatetime, getNumberOfFrames
from ..lmtanalysis.Measure import *
import sys



timeUnit = {
    'frame(s)': 1,
    'second(s)': 30,
    'minute(s)': 30*60,
    'hour(s)': 30*60*60,
    'day(s)': 30*60*60*24,
    'week(s)': 30*60*60*24*7,
}


class FileProcessException(Exception):
    pass



class FileProcessException(Exception):
    pass


def flush(connection, event='night'):
    ''' flush event in database '''
    deleteEventTimeLineInBase(connection, event)


def findFrameFromDatetime(file, theDatetime: datetime.datetime):
    """
    Check first if theDatetime is between the start and the end of the experiment: return 'outOfExperiment' if not
    Else, return the clothest FRAMENUMBER from a given datetime
    theDatetime must have a datetime format
    """
    # check if theDatetime between the start and the end of the experiment
    experimentStart = getStartInDatetime(file)
    experimentEnd = getEndInDatetime(file)
    if theDatetime < experimentStart or theDatetime > experimentEnd:
        print(f"{theDatetime} out of the experiment")
        return 'outOfExperiment'
    else:
        connection = sqlite3.connect(file)
        c = connection.cursor()
        theTimestamp = theDatetime.timestamp()*1000
        print("Searching closest frame in database....")

        query = f"SELECT FRAMENUMBER, TIMESTAMP FROM FRAME WHERE TIMESTAMP>{theTimestamp - 10000} AND TIMESTAMP<{theTimestamp + 10000}"
        c.execute(query)
        all_rows = c.fetchall()

        closestFrame = 0
        smallestDif = 100000000

        for row in all_rows:
            ts = int(row[1])
            dif = abs(ts - theTimestamp)
            if dif < smallestDif:
                smallestDif = dif
                closestFrame = int(row[0])

        connection.close()

        print("Closest Frame in selected database is: " + str(closestFrame))
        print("Distance to target: " + str(smallestDif) + " milliseconds")
        return closestFrame





def buildNightEvent(file, nightStartHour, nightEndHour, version=None):
    '''
    Rebuild night events from start time and end time (datete.time format)
    '''
    connection = sqlite3.connect(file)

    print("--------------")
    print("Current file: ", file)
    print("Flush")
    flush(connection)

    print("--------------")
    print("Loading existing events...")
    nightTimeLine = EventTimeLine(connection, "night", None, None, None, None, loadEvent=False)

    print("--------------")
    print("Event list:")
    for event in nightTimeLine.eventList:
        print(event)
    print("--------------")

    startTimeOfTheExperiment = getStartInDatetime(file)
    endTimeOfTheExperiment = getEndInDatetime(file)
    experimentTotalNumberOfFrame = getNumberOfFrames(file)

    dateStart = startTimeOfTheExperiment.date()
    # timeFromStartXpToNight = datetime.datetime.combine(dateStart, nightStartHour) - startTimeOfTheExperiment

    tempTimeStartNight = datetime.datetime.combine(dateStart, nightStartHour)
    tempTimeEndNight = datetime.datetime.combine(dateStart, nightEndHour)

    # check night period (during natural night or during day period)
    typicalCircadianRythm = tempTimeStartNight > tempTimeEndNight
    if typicalCircadianRythm:
        tempTimeEndNight = tempTimeEndNight+datetime.timedelta(days=1)
    nightDuration = tempTimeEndNight - tempTimeStartNight
    nightDurationInFrame = nightDuration.seconds*30
    timeBetweenTwoNightInFrame = timeUnit['day(s)']-nightDurationInFrame

    # experience started during light or night period
    if startTimeOfTheExperiment > tempTimeStartNight and startTimeOfTheExperiment < tempTimeEndNight:
        # experiment started during night period: startTimeOfTheExperiment is the first time for the night
        tempStartNightFrame = 0
    else:
        # experiment started during light period: tempTimeStartNight is the first time for the night
        # tempStartNightFrame = (tempTimeStartNight-startTimeOfTheExperiment).seconds*30
        tempStartNightFrame = findFrameFromDatetime(file, tempTimeStartNight)
        if tempStartNightFrame == 'outOfExperiment':
            print(f"{file}: there is no night in this experiment")
            return 'no night'
        if tempStartNightFrame > experimentTotalNumberOfFrame:
            print(f"{file}: there is no night in this experiment")
            return 'no night'

    # tempEndNightFrame = tempStartNightFrame + nightDurationInFrame
    tempEndNightFrame = findFrameFromDatetime(file, tempTimeEndNight)

    while tempStartNightFrame < experimentTotalNumberOfFrame:
        if tempEndNightFrame > experimentTotalNumberOfFrame:
            tempEndNightFrame = experimentTotalNumberOfFrame
        nightTimeLine.addEvent(Event(tempStartNightFrame, tempEndNightFrame))
        # tempStartNightFrame = tempStartNightFrame + nightDurationInFrame + timeBetweenTwoNightInFrame
        # tempEndNightFrame = tempStartNightFrame + nightDurationInFrame
        tempTimeStartNight = tempTimeStartNight + + datetime.timedelta(days=1)
        tempTimeEndNight = tempTimeEndNight + datetime.timedelta(days=1)
        tempStartNightFrame = findFrameFromDatetime(file, tempTimeStartNight)
        tempEndNightFrame = findFrameFromDatetime(file, tempTimeEndNight)
        if tempEndNightFrame == 'outOfExperiment':
            tempEndNightFrame = experimentTotalNumberOfFrame
        if tempStartNightFrame == 'outOfExperiment':
            break


    nightTimeLine.endRebuildEventTimeLine(connection)
    print(nightTimeLine.getNumberOfEvent())
    t = TaskLogger(connection)
    if version:
        print("version: "+version)
        t.addLog("Build Event Night", version=version, tmin=0, tmax=experimentTotalNumberOfFrame)
    else:
        print("no version")
        t.addLog("Build Event Night", tmin=0, tmax=experimentTotalNumberOfFrame)

    connection.close()
    print(f"{file}: night events built")





### from sensors
def getDateTime(animalPool, frame):
    if frame > 0:

        datetime = getDatetimeFromFrame(animalPool.conn, frame)
        if datetime != None:
            realTime = getDatetimeFromFrame(animalPool.conn, frame).strftime('%d-%m (%b)-%Y %H:%M:%S')
            return realTime
    return None


def process(file):
    connection = sqlite3.connect(file)

    print("--------------")
    print("Current file: ", file)

    nightTimeLine = EventTimeLine(connection, "night", None, None, None, None)
    nightTimeLine.eventList.clear()

    connection = sqlite3.connect(file)
    # build sensor data
    animalPool = AnimalPoolToolkit()
    animalPool.loadAnimals(connection)
    autoNightList = animalPool.plotSensorData(
        sensor="LIGHTVISIBLEANDIR", minValue=40, saveFile=file + "_log_light visible.pdf", show=True, autoNight=True)

    # show nights

    nightNumber = 1

    if autoNightList == None:
        print("No sensor data found.")
        return

    for autoNight in autoNightList:
        print("Night #", str(nightNumber))
        print("Starts at {} ({})".format( getDateTime(animalPool, autoNight[0]), autoNight[0]))
        print("Ends at {} ({}) ".format( getDateTime(animalPool, autoNight[1]), autoNight[1]))

        nightNumber += 1

    # ask confirmation

    answer = input("Set night(s) with autoNight data ? [y/n]:")
    if answer.lower() == "y":
        print("Setting events...")

        nightTimeLine = EventTimeLine(connection, "night", None, None, None, None)
        nightTimeLine.eventList.clear()

        for autoNight in autoNightList:
            nightTimeLine.addEvent(Event(autoNight[0], autoNight[1]))

        nightTimeLine.endRebuildEventTimeLine(connection, deleteExistingEvent=True)
        print("Setting events... Done")
    else:
        print("autoNight canceled.")




