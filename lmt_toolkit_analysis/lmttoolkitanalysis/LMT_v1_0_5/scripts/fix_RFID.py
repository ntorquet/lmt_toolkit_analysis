'''
Created on 25 Oct 2022

@author: Fab
'''
import sqlite3

from lmtanalysis.Animal import AnimalPool
from lmtanalysis.FileUtil import getFilesToProcess


def query( connection , query ):
    print( query )
    cursor = connection.cursor()
    cursor.execute( query )
    connection.commit()
    cursor.close()


def process( file ):

    print("This script let you check for RFID_A errors in database. Note that this should not happen. It means the tracker took too much time to find an animal ID.")

    print("Processing file : " , file )
    connection = sqlite3.connect( file )        
    animalPool = AnimalPool( )
    animalPool.loadAnimals( connection )


    for animal in animalPool.getAnimalList():
        if not animal.RFID.isnumeric():
            print("----")
            print("This animal is not with a valid RFID:")
            print( animal )
            print("Loading its detection:")
            animal.loadDetection( lightLoad=True )
            print("Animal number of detection: " , len( animal.detectionDictionnary ) )
            try:
                firstDetectionT = sorted(animal.detectionDictionnary.keys())[0]
                lastDetectionT = sorted(animal.detectionDictionnary.keys())[-1]
                print("First detection: ", firstDetectionT )
                print("Last detection: ", lastDetectionT )
            except:
                print("No detection associated")

            answer = input("Remove animal and IDs ? [y/n]")
            if answer.lower() == "y":
                print("Removing animal, detection and events corresponding to this animal")

                query( connection, f"DELETE FROM 'animal' WHERE id={animal.baseId}" )                
                query( connection, f"DELETE FROM 'detection' WHERE animalid={animal.baseId}" )                
                query( connection, f"DELETE FROM 'event' WHERE idanimala={animal.baseId}" )
                query( connection, f"DELETE FROM 'event' WHERE idanimalb={animal.baseId}" )
                query( connection, f"DELETE FROM 'event' WHERE idanimalc={animal.baseId}" )
                query( connection, f"DELETE FROM 'event' WHERE idanimald={animal.baseId}" )



    print("--------")

    while True:
        # reconnect
        connection = sqlite3.connect( file )        
        animalPool = AnimalPool( )
        animalPool.loadAnimals( connection )

        answer = input("Do you want to update an id of an animal ? (y/n)")
        if answer.lower() == "n":
            break

        if answer.lower() == "y":

            answer = input("What id do you want to move ?")
            sourceid = answer

            answer = input("To which id ?")
            targetid = answer

            query( connection, f"UPDATE 'animal' set id={targetid} where id={sourceid}" )
            query( connection, f"UPDATE 'detection' set animalid={targetid} where animalid={sourceid}" )
            query( connection, f"UPDATE 'event' set idanimala={targetid} where idanimala={sourceid}" )
            query( connection, f"UPDATE 'event' set idanimalb={targetid} where idanimalb={sourceid}" )
            query( connection, f"UPDATE 'event' set idanimalc={targetid} where idanimalc={sourceid}" )
            query( connection, f"UPDATE 'event' set idanimald={targetid} where idanimald={sourceid}" )









if __name__ == '__main__':

    print("This code will fix RFID problem such as RFID_A present in your experiment")

    files = getFilesToProcess()

    for file in files:
        process( file )

    print("All done.")