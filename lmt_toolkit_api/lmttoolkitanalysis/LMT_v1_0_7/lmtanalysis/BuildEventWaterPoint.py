'''
Created on 6 sept. 2017

@author: Fab
'''
import sqlite3
from time import *
from ..lmtanalysis.Chronometer import Chronometer
from ..lmtanalysis.Animal import *
from ..lmtanalysis.Detection import *
from ..lmtanalysis.Measure import *
import numpy as np
from ..lmtanalysis.Event import *
from ..lmtanalysis.Measure import *
#from affine import Affine
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from ..lmtanalysis.EventTimeLineCache import EventTimeLineCached
from ..lmtanalysis.Parameters import getAnimalTypeParameters
from ..lmtanalysis.TaskLogger import TaskLogger

def flush( connection ):
    ''' flush event in database '''
    deleteEventTimeLineInBase(connection, "Water Zone" )
    deleteEventTimeLineInBase(connection, "Water Stop" )


def reBuildEvent( connection, file, tmin=None, tmax=None, pool = None, animalType=None ): 
    
    parameters = getAnimalTypeParameters( animalType )
    
    ''' use the pool provided or create it'''
    if ( pool == None ):
        pool = AnimalPool( )
        pool.loadAnimals( connection )
        pool.loadDetection( start = tmin, end = tmax, lightLoad=True )
    '''
    Event Water Zone
    - the animal is in the zone around the water source
    - the animal is stopped in this zone for 
    '''
    
    for animal in pool.animalDictionary.keys():
        print(pool.animalDictionary[animal])
        
        eventName1 = "Water Zone"
        eventName2 = "Water Stop"
        print ( "A is in the zone around the water source")        
        print ( eventName1 )
                
        waterZoneTimeLine = EventTimeLine( None, eventName1 , animal , None , None , None , loadEvent=False )
        waterStopTimeLine = EventTimeLine( None, eventName2 , animal , None , None , None , loadEvent=False )
        
        
        stopTimeLine = EventTimeLineCached( connection, file, "Stop", animal, minFrame=None, maxFrame=None )
        stopTimeLineDictionary = stopTimeLine.getDictionary()
                
        resultWaterZone={}
        resultWaterStop={}
        
        animalA = pool.animalDictionary[animal]
        #print ( animalA )
        dicA = animalA.detectionDictionary
        
        for t in dicA.keys():
            
            dist= dicA[t].getDistanceToPoint(xPoint = 398, yPoint = 353)
            
            if dist == None:
                continue
            
            #Check if the animal is entering the zone around the water point:
            if dist <= parameters.MAX_DISTANCE_TO_POINT*2:
                resultWaterZone[t] = True
            
            #Check if the animal is drinking (the animal should be in a tight zone around the water point and be stopped):      
            if dist <= parameters.MAX_DISTANCE_TO_POINT:
                if t in stopTimeLineDictionary.keys():
                    resultWaterStop[t] = True
                
        
        waterZoneTimeLine.reBuildWithDictionary( resultWaterZone )
        waterZoneTimeLine.endRebuildEventTimeLine(connection)
        
        waterStopTimeLine.reBuildWithDictionary( resultWaterStop )
        waterStopTimeLine.removeEventsBelowLength( maxLen = parameters.MIN_WATER_STOP_DURATION )    
        waterStopTimeLine.endRebuildEventTimeLine(connection)
    
        
    # log process
    
    t = TaskLogger( connection )
    t.addLog( "Build Event Water Point" , tmin=tmin, tmax=tmax )

    print( "Rebuild event finished." )
        
        
        
        
        
        
        
    