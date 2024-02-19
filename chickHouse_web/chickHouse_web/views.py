from django.shortcuts import render
from django.http import HttpResponseRedirect
from os import getcwd
from .doorCTRL import doorCTRL
from .generatePlots import doorEvents_bar

def main_view (request) :
    door.getEventInfo()

    if request.method == 'POST' :
        if 'open_door' in request.POST :
            door.openDoor()
            print("OPEN")
            
        elif 'close_door' in request.POST :
            door.closeDoor()
        
        return HttpResponseRedirect("/dashboard/")
    
    door.reformatLastEventDT()
    # Composants à transmettre pour afficher la page
    components= {
        'locker':"🔓" if door.state else "🔒",
        'last_open':door.lastOpen,
        'last_close':door.lastClose
    }
    
    return render(request, "mainPage_chickHouse.html", components)

def statistics_view (request) :
    door.getEventInfo()

    components= {'plotView_doorEvents':doorEvents_bar(door)
    }
    
    return render(request, "statPage_chickHouse.html", components)


door = doorCTRL(True)