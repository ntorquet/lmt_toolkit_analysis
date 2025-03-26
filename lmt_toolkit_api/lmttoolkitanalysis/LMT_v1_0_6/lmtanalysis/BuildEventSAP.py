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
from ..lmtanalysis.TaskLogger import TaskLogger

def flush( connection ):
    ''' flush event in database '''
    deleteEventTimeLineInBase(connection, "SAP" )

def reBuildEvent( connection, file, tmin=None, tmax=None, pool = None , animalType = None, showGraph = False ): 
    
    ''' use the pool provided or create it'''
    if ( pool == None ):
        pool = AnimalPool( )
        pool.loadAnimals( connection )
        pool.loadDetection( start = tmin, end = tmax )
    
    
    ''' 
    Animal A is stopped (built-in event):
    Move social: animal A is stopped and in contact with any other animal.
    Move isolated: animal A is stopped and not in contact with any other animal.
    ''' 
        
    
    for animal in pool.animalDictionary:
        
        animal = pool.animalDictionary[animal]
                
        SAPTimeLine = EventTimeLine( connection, "SAP", animal.baseId, minFrame=tmin, maxFrame=tmax, loadEvent=False )

        #f = animal.getCountFramesSpecZone( start , start+oneMinute*30 , xa=143, ya=190, xb=270, yb=317 )
        result = animal.getSapDictionary( tmin , tmax )
            
        SAPTimeLine.reBuildWithDictionary( result )
        SAPTimeLine.endRebuildEventTimeLine(connection)
        #animal.clearDetection()
    
        
    # log process
    
    t = TaskLogger( connection )
    t.addLog( "Build Event SAP" , tmin=tmin, tmax=tmax )

               
    print( "Rebuild event finished." )
        
    