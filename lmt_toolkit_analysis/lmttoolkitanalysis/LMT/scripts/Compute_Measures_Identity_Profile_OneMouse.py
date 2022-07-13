'''
Created on 13 sept. 2017

@author: Fab
'''

import sqlite3
from lmtanalysis.Animal import *
import matplotlib.pyplot as plt
from lmtanalysis.Event import *
from lmtanalysis.Measure import *
from lmtanalysis import BuildEventTrain3, BuildEventTrain4, BuildEventFollowZone, BuildEventRear5, BuildEventFloorSniffing,\
    BuildEventSocialApproach, BuildEventSocialEscape, BuildEventApproachContact,\
    BuildEventApproachRear, BuildEventGroup2, BuildEventGroup3, BuildEventGroup4,\
    BuildEventStop, BuildEventWaterPoint

from tkinter.filedialog import askopenfilename
from lmtanalysis.Util import getMinTMaxTAndFileNameInput
from lmtanalysis.EventTimeLineCache import EventTimeLineCached




if __name__ == '__main__':
    
    print("Code launched.")
 
    
    behaviouralEventOneMouse = ["Contact", "Oral-oral Contact", "Oral-genital Contact", "Side by side Contact", "Side by side Contact, opposite way", "Social approach", "Social escape", "Approach contact", "Approach rear", "Break contact", "FollowZone Isolated", "Train2", "Group2", "Group3", "Group 3 break", "Group 3 make", "Group4", "Group 4 break", "Group 4 make", "Huddling", "Move isolated", "Move in contact", "Nest3", "Nest4", "Rearing", "Rear isolated", "Rear in contact", "Stop isolated", "WallJump", "Water Zone"]
    
    files = askopenfilename( title="Choose a set of file to process", multiple=1 )
    tmin, tmax, text_file = getMinTMaxTAndFileNameInput()


    for file in files:
        
        print(file)
        connection = sqlite3.connect( file )
        
        pool = AnimalPool( )
        pool.loadAnimals( connection )
        
        animalDic = {}

        for animal in pool.animalDictionnary.keys():
        
            print( "computing individual animal: {}".format( animal ))
            rfid = pool.animalDictionnary[animal].RFID
            print( "RFID: ".format( rfid ) )
            animalDic[rfid] = {}
            ''' store the animal '''
            animalDic[rfid]["animal"] = pool.animalDictionnary[animal]
            
            genoA = None
            try:
                genoA=pool.animalDictionnary[animal].genotype
            except:
                pass
                        
            for behavEvent in behaviouralEventOneMouse:
                
                print( "computing individual event: {}".format(behavEvent))    
                
                behavEventTimeLine = EventTimeLineCached( connection, file, behavEvent, animal, minFrame=tmin, maxFrame=tmax )
                
                totalEventDuration = behavEventTimeLine.getTotalLength()
                nbEvent = behavEventTimeLine.getNumberOfEvent(minFrame = tmin, maxFrame = tmax )
                print( "total event duration: " , totalEventDuration )                
                animalDic[rfid][behavEventTimeLine.eventName+" TotalLen"] = totalEventDuration
                animalDic[rfid][behavEventTimeLine.eventName+" Nb"] = nbEvent
                
                print(behavEventTimeLine.eventName, genoA, behavEventTimeLine.idA, totalEventDuration, nbEvent)
            
        print ("writing...")
        
        ''' 
        file    strain    sex    group    day    exp    idA    idB    minTime    maxTime    tot_dist
        '''
        header = ["file","strain","sex","group","day","exp","RFID","minTime","maxTime","tot_dist"]
        for name in header:
            text_file.write( "{}\t".format ( name ) ) 
        
        ''' write event keys '''
        firstAnimalKey = next(iter(animalDic))
        firstAnimal = animalDic[firstAnimalKey]
        for k in firstAnimal.keys():
            text_file.write( "{}\t".format( k.replace(" ", "") ) )
        text_file.write("\n")
        
        for kAnimal in animalDic:
            text_file.write( "{}\t".format( file ) )
            text_file.write( "{}\t".format( "strain" ) )
            text_file.write( "{}\t".format( "sex" ) )
            text_file.write( "{}\t".format( "group" ) )
            text_file.write( "{}\t".format( "day" ) )
            text_file.write( "{}\t".format( "exp" ) )
            text_file.write( "{}\t".format( animalDic[kAnimal]["animal"].RFID ) )
            text_file.write( "{}\t".format( tmin ) )
            text_file.write( "{}\t".format( tmax ) )

            COMPUTE_TOTAL_DISTANCE = True
            if ( COMPUTE_TOTAL_DISTANCE == True ):
                animalDic[kAnimal]["animal"].loadDetection( lightLoad = True )
                text_file.write( "{}\t".format( animalDic[kAnimal]["animal"].getDistance( tmin=tmin,tmax=tmax) ) )
            else:
                text_file.write( "{}\t".format( "totalDistance" ) )

            for kEvent in firstAnimal.keys():
                text_file.write( "{}\t".format( animalDic[kAnimal][kEvent] ) )
            text_file.write( "\n" )
            
        print ("done.")
            
         
                
    text_file.write( "\n" )
    text_file.close()
                
                
            
            
            