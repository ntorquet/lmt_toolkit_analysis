'''
Created on 6 sept. 2017

@author: Fab
'''
import sqlite3
from time import *

from ..experimental.Animal_LMTtoolkit import *
from ..lmtanalysis.Detection import *
from ..lmtanalysis.Measure import *
import matplotlib.pyplot as plt
import numpy as np
from ..lmtanalysis.Event import *
from ..lmtanalysis.Measure import *
from ..lmtanalysis.Chronometer import Chronometer
from ..lmtanalysis.TaskLogger import TaskLogger

def flush( connection ):
    ''' flush event in database '''
    deleteEventTimeLineInBase(connection, "Detection" )
    
    
def loadDetectionMap( connection, animal, start=None, end=None ):
    
        chrono = Chronometer("Build event detection: Load detection map")
        print( "processing animal ID: {}".format( animal ))

        result = {}
                
        cursor = connection.cursor()
        query = "SELECT FRAMENUMBER FROM DETECTION WHERE ANIMALID={}".format( animal )

        if ( start != None ):
            query += " AND FRAMENUMBER>={}".format(start )
        if ( end != None ):
            query += " AND FRAMENUMBER<={}".format(end )
            
        print( query )
        cursor.execute( query )
        
        rows = cursor.fetchall()
        cursor.close()    
        
        for row in rows:
            frameNumber = row[0]
            result[frameNumber] = True;
        
        print ( " detections loaded in {} seconds.".format( chrono.getTimeInS( )) )
        
        return result


def reBuildEvent( connection, file, tmin=None, tmax=None , pool = None, animalType = None ): 
    
    pool = AnimalPoolToolkit( )
    pool.loadAnimals( connection )
    #pool.loadDetection( start = tmin, end = tmax )
    
    for animal in range( 1 , 5 ):
        
        eventName = "Detection"        
        print ( eventName )
            
        detectionTimeLine = EventTimeLine( None, eventName , animal , None , None , None , loadEvent=False )
         
        result = loadDetectionMap( connection , animal, tmin, tmax )
                                       
        #animal = pool.animalDictionary[animal]
        #animal.loadDetection()
                    
        detectionTimeLine.reBuildWithDictionary( result );
        detectionTimeLine.endRebuildEventTimeLine(connection)
    
    # log process
    
    t = TaskLogger( connection )
    t.addLog( "Build Event Detection" , tmin=tmin, tmax=tmax )

       
    print( "Rebuild event finished." )
        
    