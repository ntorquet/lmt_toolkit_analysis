'''
Created on 13 sept. 2017

@author: Fab
'''

import sqlite3
import sys
import traceback

from lmtanalysis import BuildEventRear5, BuildEventStop, BuildEventCenterPeripheryLocation, BuildEventWaterPoint, \
    BuildEventMove, BuildEventDetection, \
    BuildDataBaseIndex, BuildEventWallJump, BuildEventSAP, \
    CheckWrongAnimal, \
    BuildEventRearCenterPeriphery
from lmtanalysis.Animal import *
from lmtanalysis.Event import *
from lmtanalysis.EventTimeLineCache import flushEventTimeLineCache, \
    disableEventTimeLineCache
from lmtanalysis.FileUtil import getFilesToProcess
from lmtanalysis.Measure import *
from lmtanalysis.TaskLogger import TaskLogger
from psutil import virtual_memory

maxT = int ( 1.5*oneHour )
USE_CACHE_LOAD_DETECTION_CACHE = True

class FileProcessException(Exception):
    pass

def process( file ):

    print(file)
    
    chronoFullFile = Chronometer("File " + file )
    
    connection = sqlite3.connect( file )        
        
    #t = TaskLogger( connection )
    #t.addLog( "Rebuild all event launch" )
                
    try:

        CheckWrongAnimal.check( connection, tmin=0, tmax=maxT )
        
        # Warning: this process will alter the lmtanalysis
        #CorrectDetectionIntegrity.correct( connection, tmin=0, tmax=maxT )
                        
        BuildDataBaseIndex.buildDataBaseIndex( connection, force=False )
            
        BuildEventDetection.reBuildEvent( connection, file, tmin=0, tmax=maxT )

        animalPool = None
        
        if ( USE_CACHE_LOAD_DETECTION_CACHE ):
            print("Caching load of animal detection...")
            animalPool = AnimalPool( )
            animalPool.loadAnimals( connection )
            animalPool.loadDetection( start = 0, end = maxT )
            print("Caching load of animal detection done.")

        
        
        chrono = Chronometer("Move" )      
        BuildEventMove.reBuildEvent( connection, file, tmin=0, tmax=maxT )
        chrono.printTimeInS()
        
        chrono = Chronometer("Rear" )      
        BuildEventRear5.reBuildEvent( connection, file, tmin=0, tmax=maxT, pool = animalPool )
        chrono.printTimeInS()
        
        chrono = Chronometer("Stop" )      
        BuildEventStop.reBuildEvent( connection, file, tmin=0, tmax=maxT )
        chrono.printTimeInS()
        
        chrono = Chronometer("Center/Periphery Zone" )      
        BuildEventCenterPeripheryLocation.reBuildEvent( connection, file, tmin=0, tmax=maxT )
        chrono.printTimeInS()
        
        chrono = Chronometer("Rear Center/Periphery" )      
        BuildEventRearCenterPeriphery.reBuildEvent( connection, file, tmin=0, tmax=maxT )
        chrono.printTimeInS()
        
        chrono = Chronometer("waterpoint" )      
        BuildEventWaterPoint.reBuildEvent(connection, file, tmin=0, tmax=maxT, pool = animalPool )
        chrono.printTimeInS()

        chrono = Chronometer("wall jump" )      
        BuildEventWallJump.reBuildEvent(connection, file, tmin=0, tmax=maxT , pool = animalPool )
        chrono.printTimeInS()

        chrono = Chronometer("sap" )      
        BuildEventSAP.reBuildEvent(connection,  file, tmin=0, tmax=maxT , pool = animalPool )
        chrono.printTimeInS()
        
        chronoFullFile.printTimeInS()
        
        
    except:
        
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        error = ''.join('!! ' + line for line in lines)
        
        t = TaskLogger( connection )
        t.addLog( error )
        
        print( error, file=sys.stderr ) 
        
        raise FileProcessException()
        

if __name__ == '__main__':
    
    print("Code launched.")
    
    mem = virtual_memory()
    availableMemoryGB = mem.total / 1000000000
    print( "Total memory on computer: (GB)", availableMemoryGB ) 
    
    if availableMemoryGB < 16:
        print( "Not enough memory to use cache load of events.")
        disableEventTimeLineCache()
    
    files = getFilesToProcess()

    chronoFullBatch = Chronometer("Full batch" )    
        
    if ( files != None ):
    
        for file in files:
            try:
                print ( "Processing file" , file )
                process( file )
            except FileProcessException:
                print ( "STOP PROCESSING FILE " + file , file=sys.stderr  )
        
            flushEventTimeLineCache()
        
    chronoFullBatch.printTimeInS()
    print( "*** ALL JOBS DONE ***")
        
        