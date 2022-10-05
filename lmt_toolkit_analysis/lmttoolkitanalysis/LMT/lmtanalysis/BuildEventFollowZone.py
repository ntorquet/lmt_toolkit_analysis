'''
Created on 6 sept. 2017

@author: Fab
'''
import sqlite3
from time import *

from affine import Affine

from .Chronometer import Chronometer
from .Animal import *
from .Detection import *
from .Measure import *
import numpy as np
from .Event import *
from .Measure import *

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from .EventTimeLineCache import EventTimeLineCached

def flush( connection ):
    ''' flush event in database '''
    deleteEventTimeLineInBase(connection, "FollowZone Isolated" )


def line( x1, x2 , y1, y2 ):
    x1, y1 = [x1, y1], [x2, y2]    
    plt.plot(x1, y1, marker = 'o')    


def checkZone ( massA_x, massA_y, angleA, meanSizeB, massB_x, massB_y, angleB ):

    dbDif= math.atan2( math.sin(angleB-angleA), math.cos(angleB-angleA) )
    dif = math.fabs( dbDif ) 

    if ( dif < math.pi/4):
        #transfer the referential: position of B in the new space
        x,y = transformPoint(angleB, massA_x, massA_y, massB_x, massB_y)
        #print(x,y)
        
        if (x>-0.5*meanSizeB and x<0.5*meanSizeB and y>-meanSizeB and y<0):
        #if ( x >-20 and x < 20 and y > -100 and y < 0 ):
            return True

    
def transformPoint(angleB, massA_x, massA_y, massB_x, massB_y):
    '''
    transform the origin of the space so that the mass center of animalB is the origin of the new space
    '''
 
    Affine.identity()

    x = massA_x - massB_x
    y = massA_y - massB_y

    rotation = Affine.rotation(90- math.degrees( angleB ) ) * ( x , y )
    
    return rotation[0], rotation[1]


def reBuildEvent( connection, file, tmin=None, tmax=None, pool = None ): 
    
    ''' use the pool provided or create it'''
    if ( pool == None ):
        pool = AnimalPool( )
        pool.loadAnimals( connection )
        pool.loadDetection( start = tmin, end = tmax )

    '''
    Event FollowZone:
    - the two animals are moving at a speed >5 cm/s (SPEED_THRESHOLD_LOW)
    - the angles between the two animals are less than 45° apart
    - the mass center of the follower is within a follow zone of one mean body length of width and two mean body lengths of length
    - either the animal B is in contact with another one (FollowZone Social) or the animal B is not in contact with any other animal (except A at the end of the follow event; FollowZone Isolated)
    
    - update 17 may 2018: now works with n animals    
    
    '''
    
    contact = {}
    
    for idAnimalB in pool.animalDictionnary.keys():
        print(pool.animalDictionnary[idAnimalB])
        #meanSizeB = pool.animalDictionnary[idAnimalB].getMeanBodyLength( tmax = tmax )
        
        for animal in pool.animalDictionnary.keys():
            if( idAnimalB == animal ):
                continue
            
            contact[animal, idAnimalB] = EventTimeLineCached( connection, file, "Contact", animal, idAnimalB, minFrame=tmin, maxFrame=tmax )
            #contact[idAnimalB] = EventTimeLine( connection, "Contact", idAnimalB )
    
    for idAnimalB in pool.animalDictionnary.keys():
        
        meanSizeB = pool.animalDictionnary[idAnimalB].getMeanBodyLength( tmax = tmax )
        
        for animal in pool.animalDictionnary.keys():
            if( animal == idAnimalB ):
                continue
    
            allAnimals = list( pool.animalDictionnary.keys() )
            allAnimals.remove( animal )
            allAnimals.remove( idAnimalB )
            allOtherAnimals = allAnimals 
    
            eventName = "FollowZone Isolated"
        
            print ( "A follow B")        
            print ( eventName )
                    
            followIsolatedTimeLine = EventTimeLine( None, eventName , animal , idAnimalB , None , None , loadEvent=False )
            print( followIsolatedTimeLine.eventNameWithId ) 
                    
            resultIso={}
            
            animalA = pool.animalDictionnary[animal]
            animalB = pool.animalDictionnary[idAnimalB]

            dicA = animalA.detectionDictionnary
            dicB = animalB.detectionDictionnary
            
            dicContactBToOtherAnimal = {}
            for idOtherAnimal in allOtherAnimals :                
                dicContactBToOtherAnimal[ idOtherAnimal ] = contact[ idAnimalB, idOtherAnimal ].getDictionnary() 
            
            #dicContactBC = contact[ idAnimalB, idAnimalC ].getDictionnary()
            #dicContactBD = contact[ idAnimalB, idAnimalD ].getDictionnary()
            
            for t in dicB.keys():
                
                testContactWithOtherAnimal=False

                for idOtherAnimal in allOtherAnimals :
                    if ( t in dicContactBToOtherAnimal[ idOtherAnimal ] ):
                        testContactWithOtherAnimal = True
                        break
                
                if testContactWithOtherAnimal==True:
                    continue
                
                '''
                if ( t in dicContactBC.keys() or t in dicContactBD ):
                    continue
                '''
               
                if ( t in dicA.keys() ):
                
                    
                    speedA = pool.animalDictionnary[animal].getSpeed(t)
                    speedB = pool.animalDictionnary[idAnimalB].getSpeed(t)
                    #angleB = pool.animalList[idAnimalB].getDirection(t)
                    if not pool.animalDictionnary[animal].getDetectionAt( t ).isHeadAndTailDetected():
                        continue
                    angleA = pool.animalDictionnary[animal].getDirection(t)
                    
                    if (speedA == None or speedB == None):
                        continue
                    
                    if ( speedA>SPEED_THRESHOLD_LOW and speedB>SPEED_THRESHOLD_LOW ):

                        time = t
                        angleB = pool.animalDictionnary[idAnimalB].getDirection(time)

                        '''
                        try:                                    
                            if( animalA.getDistanceTo( t, animalB ) > 80 ):
                                continue
                        except:
                            continue
                        '''
                        
                        
                        for time in range( t-15, t+1, 2):
                        #time = t
                            try:
                                if pool.animalDictionnary[idAnimalB].getDetectionAt( time ).isHeadAndTailDetected():
                                    angleB = pool.animalDictionnary[idAnimalB].getDirection(time)
                                    if ( checkZone( dicA[t].massX, dicA[t].massY, angleA, meanSizeB, dicB[time].massX, dicB[time].massY, angleB ) == True):
             
                                        resultIso[t] = True
                                        break
                            except:
                                pass                
                    
                        
                    
            followIsolatedTimeLine.reBuildWithDictionnary( resultIso )
            
            followIsolatedTimeLine.endRebuildEventTimeLine(connection)
    
        
    # log process
    from .TaskLogger import TaskLogger
    t = TaskLogger( connection )
    t.addLog( "Build Event Follow Zone" , tmin=tmin, tmax=tmax )

              
    print( "Rebuild event finished." )
        
    