'''
Created on 6 sept. 2017

@author: Fab
'''
import sqlite3
from time import *

from affine import Affine

from ..lmtanalysis.Chronometer import Chronometer
from ..experimental.Animal_LMTtoolkit import AnimalPoolToolkit as AnimalPool
from ..lmtanalysis.Detection import *
#from ..lmtanalysis.Measure import  SPEED_THRESHOLD_LOW
import numpy as np
from ..lmtanalysis.Event import *
from ..lmtanalysis.Measure import *

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from ..lmtanalysis.EventTimeLineCache import EventTimeLineCached
import copy
from copy import deepcopy
from ..lmtanalysis.Parameters import getAnimalTypeParameters
from ..lmtanalysis.TaskLogger import TaskLogger

#eventName = "FollowZone New4"
eventName = "FollowZone"
            
def flush( connection ):
    ''' flush event in database '''
    print("Flushing " , eventName )
    deleteEventTimeLineInBase(connection, eventName )
    print("Flushing " , "FollowZone Isolated" )
    deleteEventTimeLineInBase(connection, "FollowZone Isolated"  )


def isSameWay( detA, detB ):
    
    vectAX = detA.frontX - detA.backX
    vectAY = detA.frontY - detA.backY

    vectBX = detB.frontX - detB.backX
    vectBY = detB.frontY - detB.backY
    
    scalarProduct = vectAX * vectBX + vectAY * vectBY
    
    if ( scalarProduct >= 0 ): #same direction
        return True
    
    return False

def isAFollowingB( t , dicA , dicB, parameters ):
    
    # False is detection A does not exist at t
    if t not in dicA:
        return False
    
    # False is detection B does not exist at t
    if t not in dicB:
        return False
    
    # False if at least for the current t animals are not in the same direction. Could be wrong if animals are spinning around while following but filters out a number of complex situation
    if not isSameWay( dicA[t], dicB[t] ):
        return False
        
    detectionA = dicA[t]
    
    # check if in the past B was in A location
    for timeB in range( t-parameters.FOLLOW_CORRIDOR_DURATION,t+1 ):
        
        # check if detection B exists:
        if not timeB in dicB:
            continue
        
        detectionB = dicB[timeB]
        
        distance = detectionA.getDistanceTo( detectionB, parameters )  

        # discard invalid distances
        if distance == None:
            continue
                
        # discard if distance is too large between detections
        if distance > parameters.FOLLOW_DISTANCE_MAX_PIX:

            continue
                         
        # discard if animals are not going the same way ( scalar test )
        if not isSameWay( detectionA, detectionB ):
            continue
        
        # discard if angle between animals is not ok
        angleA = detectionA.getDirection()
        angleB = detectionB.getDirection()
        dbDif= math.atan2( math.sin(angleB-angleA), math.cos(angleB-angleA) )
        dif = math.fabs( dbDif )
        if ( dif > parameters.FOLLOW_MAX_ANGLE ):
            continue
        
        
        return True
        
    
    
    
    return False
    

def reBuildEvent( connection, file, tmin=None, tmax=None, pool = None, animalType = None ): 
    
    '''
    Event FollowZone:
    - ok: the two animals are moving at a speed >5 cm/s (SPEED_THRESHOLD_LOW)
    - ok: animals must not be in contact
    
    - ok: the angles between the two animals are less than 45 degrees apart considering head tail direction
    
    '''
    
    parameters = getAnimalTypeParameters( animalType )
    
    
    # create dedicated pool as we will alter detection pool with filters (I.e: we don't use the pool cache)
    
    pool = AnimalPool( )
    pool.loadAnimals( connection )
    pool.loadDetection( start = tmin, end = tmax )
    
    # filter detection by speed. Keep only the detection that are over SPEED_THRESHOLD_LOW.
    #pool.filterDetectionByInstantSpeed( pool.getAnimalList()[0].parameters.SPEED_THRESHOLD_LOW , 1000 ) # for the rat compatible version
    #pool.filterDetectionByInstantSpeed( SPEED_THRESHOLD_LOW*2 , 1000 )
    pool.filterDetectionByInstantSpeed( parameters.SPEED_THRESHOLD_LOW*parameters.FOLLOW_SPEED_MULTIPLICATOR_THRESHOLD , 1000 )
    
    # remove all detection where head and tail are missing
    pool.filterDetectionToKeepOnlyHeadTailDetection()
    
    
    # load the contact matrix dictionary    
    contactDic = {}    
    oralGenitalDic = {}
    for idAnimalA in pool.animalDictionary:
        print(pool.animalDictionary[idAnimalA])
        for idAnimalB in pool.animalDictionary:
            if( idAnimalA == idAnimalB ):
                continue
            contactDic[idAnimalA, idAnimalB] = EventTimeLineCached( connection, file, "Contact", idAnimalA, idAnimalB, minFrame=tmin, maxFrame=tmax ).getDictionary()    
            oralGenitalDic[idAnimalA, idAnimalB] = EventTimeLineCached( connection, file, "Oral-genital Contact", idAnimalA, idAnimalB, minFrame=tmin, maxFrame=tmax ).getDictionary()
            
    #init empty result EventTimeLine matrix
    followIsolatedTimeLine = {}
    for idAnimalA in pool.animalDictionary:
        for idAnimalB in pool.animalDictionary:
            if( idAnimalA == idAnimalB ):
                continue                                        
            followIsolatedTimeLine[idAnimalA, idAnimalB] = EventTimeLine( None, eventName , idAnimalA , idAnimalB , None , None , loadEvent=False )

    # init empty result timeline Dictionary.
    followIsolatedTimeLineDic = {}
    
    for idAnimalA in pool.animalDictionary:

        animalA = pool.animalDictionary[idAnimalA]
        dicA = animalA.detectionDictionary
        
        for idAnimalB in pool.animalDictionary:
            
            # discard if animals are the same.
            if( idAnimalA == idAnimalB ):
                continue
            
            # result dictionary for the current pair tested.            
            resultDic = {}

            animalB = pool.animalDictionary[idAnimalB]
            dicB = animalB.detectionDictionary
            
            # Starting "is A following B ?"
                        
            for t in dicB:            
                if isAFollowingB( t , dicA , dicB, parameters ):
                    resultDic[t]=True

            # remove all contact situation
            for t in contactDic[idAnimalA, idAnimalB]:
                if t in resultDic:
                    resultDic.pop( t )
            
            for t in oralGenitalDic[idAnimalA, idAnimalB]:
                if t in resultDic:
                    resultDic.pop( t )
            
            for t in oralGenitalDic[idAnimalB, idAnimalA]:
                if t in resultDic:
                    resultDic.pop( t )
            
            followIsolatedTimeLineDic[idAnimalA, idAnimalB] = resultDic

            
    #rebuild timelines with dictionaries
    for idAnimalA in pool.animalDictionary:
        for idAnimalB in pool.animalDictionary:
            if( idAnimalB == idAnimalA ):
                continue
            followIsolatedTimeLine[idAnimalA, idAnimalB].reBuildWithDictionary( followIsolatedTimeLineDic[idAnimalA, idAnimalB] )
                        
            # filter out accidental events
            followIsolatedTimeLine[idAnimalA, idAnimalB].removeEventsBelowLength( parameters.FOLLOW_REMOVE_EVENT_BELOW_LEN )
            # create continuity in the events
            followIsolatedTimeLine[idAnimalA, idAnimalB].mergeCloseEvents( parameters.FOLLOW_MERGE_EVENT_LEN_CRITERIA )
                        
            followIsolatedTimeLine[idAnimalA, idAnimalB].endRebuildEventTimeLine(connection)
                
    # log process
    
    t = TaskLogger( connection )
    t.addLog( eventName , tmin=tmin, tmax=tmax )
              
    print( "Rebuild event finished." )
    return
    
            
    
            
        
        
    