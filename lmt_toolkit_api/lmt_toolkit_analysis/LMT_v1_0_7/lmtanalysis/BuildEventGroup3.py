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
from ..lmtanalysis.EventTimeLineCache import EventTimeLineCached
from ..lmtanalysis.TaskLogger import TaskLogger

def flush( connection ):
    ''' flush event in database '''
    deleteEventTimeLineInBase(connection, "Group3" )


def reBuildEvent( connection, file, tmin=None, tmax=None, pool = None, animalType = None  ):
    
    pool = AnimalPoolToolkit( )
    pool.loadAnimals( connection )
    #pool.loadDetection( start = tmin, end = tmax )
    
    if pool.getNbAnimals() <= 2:
        print( "Not enough animals to process group 3")
        return

    contact = {}
    for animal in range( 1 , 5 ):
        for idAnimalB in range( 1 , 5 ):
            if ( animal == idAnimalB ):
                continue
            contact[animal, idAnimalB] = EventTimeLineCached( connection, file, "Contact", animal, idAnimalB, minFrame=tmin, maxFrame=tmax )

    for animal in range( 1 , 5 ):
        
        for idAnimalB in range( 1 , 5 ):
            if( animal == idAnimalB ):
                continue
            
            for idAnimalC in range( 1 , 5 ):
                if( animal == idAnimalC ):
                    continue
                if( idAnimalB == idAnimalC ):
                    continue
                
                for idAnimalD in range( 1 , 5 ):
                    if( animal == idAnimalD ):
                        continue
                    if( idAnimalB == idAnimalD ):
                        continue
                    if( idAnimalC == idAnimalD ):
                        continue
                
                    eventName = "Group3"        
                    print ( eventName )
                    
                    groupTimeLine = EventTimeLine( None, eventName , animal , idAnimalB , idAnimalC , None , loadEvent=False )
                    
                    result={}
                    
                    dicAB = contact[ animal , idAnimalB ].getDictionary()
                    dicAC = contact[ animal , idAnimalC ].getDictionary()
                    dicAD = contact[ animal , idAnimalD ].getDictionary()
                    dicBC = contact[ idAnimalB , idAnimalC ].getDictionary()
                    dicBD = contact[ idAnimalB , idAnimalD ].getDictionary()
                    dicCD = contact[ idAnimalC , idAnimalD ].getDictionary()
                    
                    for t in dicAB.keys():
                        if ( t in dicAC or t in dicBC ):
                            if ( t in dicAD or t in dicBD or t in dicCD ):
                                continue
                            else:
                                result[t]=True
                    
                    for t in dicAC.keys():   
                        if ( t in dicBC ):
                            if ( t in dicAD or t in dicBD or t in dicCD ):
                                continue
                            else:
                                result[t]=True
                    
                groupTimeLine.reBuildWithDictionary( result )
                
                groupTimeLine.endRebuildEventTimeLine(connection)
                    
        
    # log process
    
    t = TaskLogger( connection )
    t.addLog( "Build Event Group 3" , tmin=tmin, tmax=tmax )
      
                    
    print( "Rebuild event finished." )
        
    