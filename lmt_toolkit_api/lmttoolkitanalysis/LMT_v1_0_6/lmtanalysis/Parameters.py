'''
Created on 20 dec. 2022

@author: Fab
'''
from ..lmtanalysis.AnimalType import AnimalType
from ..lmtanalysis.ParametersMouse import ParametersMouse
from ..lmtanalysis.ParametersRat import ParametersRat


def getAnimalTypeParameters( animalType ):
    print(f"---------- parameters for animalType: {animalType} ----------")

    if animalType == AnimalType.MOUSE:
        print("gna!")
        return ParametersMouse()

    if animalType == AnimalType.RAT:
        return ParametersRat()

    if animalType:
        print(f"---------- condition parameters for animalType: {animalType} ----------")
        if animalType == AnimalType.MOUSE:
            print("ben alors?!")
        else:
            print(isinstance(animalType, AnimalType))

    print(f"Error: animal type is None: {animalType}")
    quit()
    


    return None