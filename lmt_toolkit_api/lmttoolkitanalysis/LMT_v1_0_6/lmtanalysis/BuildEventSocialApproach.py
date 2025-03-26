'''
Created on 6 sept. 2017

@author: Fab
'''
import sqlite3
from time import *
from ..lmtanalysis.Chronometer import Chronometer
from ..experimental.Animal_LMTtoolkit import AnimalPoolToolkit as AnimalPool
from ..lmtanalysis.Detection import *
from ..lmtanalysis.Measure import *
import matplotlib.pyplot as plt
import numpy as np
from ..lmtanalysis.Event import *
from ..lmtanalysis.Measure import *
from ..lmtanalysis.EventTimeLineCache import EventTimeLineCached
from ..lmtanalysis.TaskLogger import TaskLogger

def flush( connection ):
    ''' flush event in database '''
    deleteEventTimeLineInBase(connection, "Social approach" )


def reBuildEvent( connection, file, tmin=None, tmax=None, pool = None, animalType = None ): 
    
    ''' use the pool provided or create it'''
    if ( pool == None ):
        pool = AnimalPool( )
        pool.loadAnimals( connection )
        pool.loadDetection( start = tmin, end = tmax )
    
    
    approachDico = {}
    for animal in range( 1 , pool.getNbAnimals()+1 ):
        for idAnimalB in range( 1 , pool.getNbAnimals()+1 ):
            if ( animal == idAnimalB ):
                continue
            approachDico[animal, idAnimalB] = EventTimeLineCached( connection, file, "Approach", animal, idAnimalB, minFrame=tmin, maxFrame=tmax ) 
            
    #cache mean body len
    twoMeanBodyLen = {}
    for idAnimal in range( 1 , pool.getNbAnimals()+1 ):
        meanBodyLength = pool.animalDictionary[idAnimal].getMeanBodyLength()
        # init value
        twoMeanBodyLen[idAnimal] = None
        #set body length
        if meanBodyLength != None:
            twoMeanBodyLen[idAnimal] = 2*meanBodyLength
        
    for animal in range( 1 , pool.getNbAnimals()+1 ):
        
        for idAnimalB in range( 1 , pool.getNbAnimals()+1 ):
            if( animal == idAnimalB ):
                continue
            
            if twoMeanBodyLen[idAnimalB] == None:
                print("Social Approach: can't compute mean bodyLen. Skip animal." )
                continue
            
            eventName = "Social approach"        
            print ( eventName )
            
            socAppTimeLine = EventTimeLine( None, eventName , animal , idAnimalB , None , None , loadEvent=False )
                           
            result={}
            
            dicA = approachDico[ animal , idAnimalB ].getDictionary()
            
            twoMeanBodyLengthB = twoMeanBodyLen[ idAnimalB ]
            
            for t in dicA.keys():
                
                dist = pool.animalDictionary[animal].getDistanceTo(t, pool.animalDictionary[idAnimalB])
                
                if ( dist == None ):
                    continue
                    
                if ( dist >= 0 and dist <= twoMeanBodyLengthB ):
                    
                    result[t]=True
            
            
            socAppTimeLine.reBuildWithDictionary( result )
            
            socAppTimeLine.endRebuildEventTimeLine(connection)
    
        
    # log process
    
    t = TaskLogger( connection )
    t.addLog( "Build Event Social Approach" , tmin=tmin, tmax=tmax )

        
    print( "Rebuild event finished." )
        
    