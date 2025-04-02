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
from ..lmtanalysis.TaskLogger import TaskLogger

def flush( connection ):
    ''' flush event in database '''
    deleteEventTimeLineInBase(connection, "Floor sniffing" )


def reBuildEvent( connection, tmin, tmax , pool = None, animalType = None ): 
    '''
    Event Floor sniffing:
    - the animal is sniffing the floor
    '''
    
    pool = AnimalPool( )
    pool.loadAnimals( connection )
    pool.loadDetection( start = tmin, end = tmax )
    
    for animal in pool.animalDictionary.keys():
        print(pool.animalDictionary[animal])
        
        eventName = "Floor sniffing"
        print ( "A sniffs the floor")        
        print ( eventName )
                
        sniffFloorTimeLine = EventTimeLine( None, eventName , animal , None , None , None , loadEvent=False )
                
        result={}
        
        animalA = pool.animalDictionary[animal]
        #print ( animalA )
        dicA = animalA.detectionDictionary
            
        for t in dicA.keys():
            if (animalA.getBodySlope(t) == None):
                continue
            
            if (animalA.getBodySlope(t) >= -25 and animalA.getBodySlope(t) <= -15):
                #print("floor sniffing")
                result[t] = True
                
        
        sniffFloorTimeLine.reBuildWithDictionary( result )
                
        sniffFloorTimeLine.endRebuildEventTimeLine(connection)
    
        
    # log process
    
    t = TaskLogger( connection )
    t.addLog( "Build Event Floor sniffing" , tmin=tmin, tmax=tmax )

    print( "Rebuild event finished." )
        
        
        
        
        
        
        
    