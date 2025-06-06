'''
Created on 6 sept. 2017

@author: Fab
'''
import sqlite3
from time import *
from ..lmtanalysis.Chronometer import Chronometer
from ..experimental.Animal_LMTtoolkit import *
from ..lmtanalysis.Detection import *
from ..lmtanalysis.Measure import *
import matplotlib.pyplot as plt
import numpy as np
from ..lmtanalysis.Event import *
from ..lmtanalysis.Measure import *
from ..lmtanalysis.TaskLogger import TaskLogger

def flush( connection ):
    ''' flush event in database '''
    deleteEventTimeLineInBase(connection, "Huddling" )

def reBuildEvent( connection, file, tmin=None, tmax=None, pool = None , animalType = None, showGraph = False ): 
    
    ''' use the pool provided or create it'''
    if ( pool == None ):
        pool = AnimalPoolToolkit( )
        pool.loadAnimals( connection )
        #pool.loadDetection( start = tmin, end = tmax )
    
    
    for idAnimalA in pool.animalDictionary:
        
        threshold = 0.5
        animal = pool.animalDictionary[idAnimalA]
        print("Computing huddling for animal " , animal )
                
        huddlingTimeLine = EventTimeLine( connection, "Huddling", idAnimalA, minFrame=tmin, maxFrame=tmax, loadEvent=False )

        result = {}
        
        for t in range( tmin, tmax+1 ):
            if t%10000 == 0:
                print ( "current t", t )
                            
            mask = animal.getBinaryDetectionMask( t )
            if mask == None:
                continue
            roundness = mask.getRoundness()
            if roundness == None:
                continue
            #print ( idAnimalA , t , roundness )
            #if roundness > 1-threshold and roundness < 1+threshold:
            if roundness < 1.85: # and roundness > 1:
                result[t] = True  
            
        huddlingTimeLine.reBuildWithDictionary( result )
        huddlingTimeLine.endRebuildEventTimeLine(connection)
    
        
    # log process
    
    t = TaskLogger( connection )
    t.addLog( "Build Event Huddling" , tmin=tmin, tmax=tmax )

               
    print( "Rebuild event finished." )
        
    