'''
Created on 13 sept. 2017

@author: Fab
'''
from ..lmtanalysis.Point import Point
from ..lmtanalysis.Measure import oneSecond, oneMinute
import math

class ParametersRat():

    ''' scale to convert distances from pixels to cm '''
    scaleFactor = 20/57
    
    ''' '''
    SPEED_THRESHOLD_LOW = 5
    SPEED_THRESHOLD_HIGH = 10
    
    ''' threshold for a mean speed over a time period '''
    AVERAGE_HIGH_SPEED_THRESHOLD = 19
    
    ''' speed threshold to define high speed movements '''
    HIGH_SPEED_MOVE_THRESHOLD = 18
    MAXIMUM_SPEED_THRESHOLD = 300
    
    ''' slope of the body between the nose and the tail basis '''
    BODY_SLOPE_THRESHOLD = 40
    
    ''' threshold for the distance contact using mass center between two detection '''
    DISTANCE_CONTACT_MASS_CENTER = 8/scaleFactor
    
    ''' threshold for the maximum distance allowed between two points '''
    MAX_DISTANCE_THRESHOLD = 71/scaleFactor
    
    '''distance between the two animals to compute the follow behaviour'''
    FOLLOW_DISTANCE_MAX_PIX = 8.5/scaleFactor # numeric value in cm to obtain pixels
    FOLLOW_CORRIDOR_DURATION = 50 # in frames
    FOLLOW_MAX_ANGLE = math.pi/4 # in radians
    FOLLOW_SPEED_MULTIPLICATOR_THRESHOLD = 1.5
    FOLLOW_REMOVE_EVENT_BELOW_LEN = 7 # in frames        
    FOLLOW_MERGE_EVENT_LEN_CRITERIA = 10 # in frames

    # vibrisae size in cm 
    VIBRISSAE = 3
    
    ''' threshold min time after a first rearing to detect the second rearing (frames)'''
    SEQUENTIAL_REARING_MIN_TIME_THRESHOLD = 10
    
    ''' threshold max time after a first rearing to detect the second rearing (frames)'''
    SEQUENTIAL_REARING_MAX_TIME_THRESHOLD = 30
    
    ''' threshold for the area around a reared animal for sequential rearing '''
    SEQUENTIAL_REARING_POSITION_THRESHOLD = 50
    
    ''' threshold for the presence within the water zone '''
    MAX_DISTANCE_TO_WATER_POINT = 11/scaleFactor 
    
    ''' threshold for the presence within the water zone to drink'''
    MAX_DISTANCE_TO_WATER_NOSE_POSITION = 3/scaleFactor 
    
    ''' threshold for the presence within the gate zone to enter'''
    MAX_DISTANCE_TO_GATE_NOSE_ENTRANCE = 3/scaleFactor 
    
    ''' threshold for the presence within the gate zone '''
    MAX_DISTANCE_TO_GATE_POINT = 11/scaleFactor
    
    ''' threshold for the presence within the wheel zone '''
    MAX_DISTANCE_TO_WHEEL_POINT = 11/scaleFactor 
    
    ''' water zone's coordinates'''
    X_WATER_POINT = 123
    Y_WATER_POINT = 82
    
    ''' gate zone's coordinates'''
    X_GATE_POINT = 165
    Y_GATE_POINT = 352
    
    ''' wheel zone's coordinates'''
    X_WHEEL_POINT = 248
    Y_WHEEL_POINT = 106
    
    ''' distance to an object, to take into account the vibrissae length '''
    DISTANCE_TO_OBJECT_NOR = 3 / scaleFactor
    
    ''' threshold to classify the detection as a rearing; height of the front point'''
    FRONT_REARING_THRESHOLD = 50
    
    ''' threshold to compute head-genital events '''
    MAX_DISTANCE_HEAD_HEAD_GENITAL_THRESHOLD = 15
    
    ''' time window for oral-side sequences '''
    TIME_WINDOW_ORAL_SIDE_SEQUENCE = 60
    
    ''' time window after an event to look for other events '''
    TIME_WINDOW_AFTER_EVENT = 1*oneMinute
    
    ''' time window after a contact to look for the beginning of a get away '''
    TIME_WINDOW_AFTER_CONTACT = 10
    
    ''' minimal duration of events to be considered (for example in oral-side sequences) '''
    EVENT_MIN_DURATION = 10
    
    ''' Minimum duration of stay in a corner to be considered as a corner event (frames)'''
    MIN_DURATION_IN_CORNER = 180
    
    ''' Minimum duration for the animal to stop at the water point to be classified as drinking '''
    MIN_WATER_STOP_DURATION = 2*oneSecond
    
    ''' Minimum duration for the animal to stop at the gate point to be classified as drinking '''
    MIN_GATE_STOP_DURATION = 2*oneSecond
     
    ''' Cage center in 100x100cm area'''
    cageCenterCoordinatesOpenFieldArea = Point( 256, 208 )
    
    ''' Size of arena in cm '''
    ARENA_SIZE = 100
    
    ''' Margin to define center region in cm (chosen to have same area as non-center)'''
    CENTER_MARGIN = 14.64
    
    ''' Corner Coordinates in 100x100cm area '''
    cornerCoordinatesOpenFieldArea = [
                            (114,63),
                            (398,63),
                            (398,353),
                            (114,353)
                            ]

    ''' Margin to define whole cage area without a border in cm '''
    # TODO check value for the rat
    CAGE_MARGIN = 6


