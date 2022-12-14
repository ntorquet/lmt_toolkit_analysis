'''
Created on 12 dec 2019

@author: Fab
'''

import sqlite3
from lmtanalysis.Animal import *
import matplotlib.pyplot as plt
from lmtanalysis.Event import *
from lmtanalysis.Measure import *

from tkinter.filedialog import askopenfilename
from lmtanalysis.TaskLogger import TaskLogger
import sys
import traceback
from lmtanalysis.FileUtil import getFilesToProcess

from lmtanalysis.EventTimeLineCache import EventTimeLineCached

def process( file ):

    print(file)
        
    
    connection = sqlite3.connect( file )
    
    c = connection.cursor()
    query = "ALTER TABLE ANIMAL ADD AGE TEXT";
    c.execute( query )
    query = "ALTER TABLE ANIMAL ADD SEX TEXT";
    c.execute( query )
    query = "ALTER TABLE ANIMAL ADD STRAIN TEXT";
    c.execute( query )
    query = "ALTER TABLE ANIMAL ADD SETUP TEXT";
    c.execute(query)
    connection.commit()
    c.close()
    connection.close()

    

def processAll():
    
    
    files = getFilesToProcess()

    chronoFullBatch = Chronometer("Full batch" )    
        
    if ( files != None ):
    
        for file in files:
                print ( "Processing file" , file )
                process( file )
        
    chronoFullBatch.printTimeInS()
    print( "*** ALL JOBS DONE ***")

if __name__ == '__main__':
    
    print("Code launched.")
    processAll()
    