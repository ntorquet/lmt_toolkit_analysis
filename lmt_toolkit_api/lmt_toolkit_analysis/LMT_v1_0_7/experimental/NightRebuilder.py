'''
Created by Nicolas Torquet at 24/06/2025
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
'''

'''
This script manage the rebuild of night event.
There is several ways to do this:
1. from sensors: the data have to be verified by the user
2. from start hour and end hour of the night: user has to provide those information
3. from start hour and for a duration: user has to provide those information
'''

import datetime


timeUnit = {
    'frame(s)': 1,
    'second(s)': 30,
    'minute(s)': 30*60,
    'hour(s)': 30*60*60,
    'day(s)': 30*60*60*24,
    'week(s)': 30*60*60*24*7,
}


class NightModel:
    def __init__(self, start_hour: str, end_hour: str):
        self.start_hour = datetime.datetime.strptime(start_hour, "%H:%M:%S")
        self.end_hour = datetime.datetime.strptime(end_hour, "%H:%M:%S")
        if self.start_hour < self.end_hour:
            self.duration = self.end_hour - self.start_hour
        else:
            self.duration = (self.end_hour - self.start_hour) % datetime.timedelta(days=1)


    def getStartHour(self):
        return self.startHour

    def getEndHour(self):
        return self.endHour

    def getDuration(self):
        return self.duration



class Night(NightModel):
    def __init__(self, night_model: NightModel, start_date: str, end_date: str):
        self.night_model = night_model
        self.start_date = datetime.datetime.strptime(start_date, "%Y/%m/%d %H:%M:%S")
        self.end_date = datetime.datetime.strptime(end_date, "%Y/%m/%d %H:%M:%S")
        NightModel.__init__(self, start_hour=self.start_date.strftime('%H:%M:%S'), end_hour=self.end_date.strftime('%H:%M:%S'))

    def getStartDate(self):
        return self.start_date

    def getEndDate(self):
        self.end_date





class NightPool:
    def __init__(self, night_model: NightModel):
        self.night_list = []
        self.nighModel = night_model

    def addNight(self, nigh: Night):
        self.night_list.append(nigh)




if __name__ == '__main__':
    start_hour = input('Start night hour (like 08:00:00): ')
    end_hour = input('End night hour (like 08:00:00): ')
    night_model = NightModel(start_hour, end_hour)

