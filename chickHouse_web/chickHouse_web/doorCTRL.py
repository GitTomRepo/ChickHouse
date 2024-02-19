from os import getcwd
import pandas as pd
import datetime
import subprocess

'''
df_events Format :
DateTimeEvent   TypeEvent
'''

class doorCTRL () :
    lastOpen = ""
    lastClose = ""
    df_events = pd.DataFrame()

    def __init__ (self, state_door:bool=True) :
        self.state = state_door # True = ouvert | False = fermé

    def closeDoor (self) :
        self.state = False
        new_row = {'DateTimeEvent':datetime.datetime.now(), 
           'TypeEvent':False}
        
        self.df_events = pd.concat([self.df_events, pd.DataFrame([new_row])], ignore_index=True)
        self.df_events.to_csv(getcwd() + "\\chickHouse_web\\" + "eventDoor.csv", index=False)  

    def openDoor (self) :
        self.state = True
        new_row = {'DateTimeEvent':datetime.datetime.now(), 
           'TypeEvent':True}
        
        self.df_events = pd.concat([self.df_events, pd.DataFrame([new_row])], ignore_index=True)
        self.df_events.to_csv(getcwd() + "\\chickHouse_web\\" + "eventDoor.csv", index=False)  
        proc_open = subprocess.Popen(['python', getcwd() + '\\PY_GPIOscript\\OPEN_door.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def getEventInfo (self) :
        self.df_events = pd.read_csv(getcwd() + "\\chickHouse_web\\" + "eventDoor.csv")
        self.df_events['DateTimeEvent']= pd.to_datetime(self.df_events['DateTimeEvent'])

        if 'DateTimeEvent' in self.df_events.columns :
            self.lastOpen = self.df_events[self.df_events['TypeEvent'] == True].iloc[-1]['DateTimeEvent']
            self.lastClose = self.df_events[self.df_events['TypeEvent'] == False].iloc[-1]['DateTimeEvent']

        proc_close = subprocess.Popen(['python', getcwd() + '\\PY_GPIOscript\\CLOSE_door.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def reformatLastEventDT (self) :
        months = ["janvier", "février", "mars", "avril", "mais", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

        self.lastOpen = f"{self.lastOpen.day} {months[self.lastOpen.month - 1]} {self.lastOpen.year} - {self.lastOpen.hour}h{self.lastOpen.minute}"
        self.lastClose = f"{self.lastClose.day} {months[self.lastClose.month - 1]} {self.lastClose.year} - {self.lastClose.hour}h{self.lastClose.minute}"