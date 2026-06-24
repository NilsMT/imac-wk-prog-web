import model.event
import sqlite3

def createEvent(data_event, id_user):
    try :
        model.event.insertEvent(data_event, id_user)
        return "Event created successfully", 201
    except sqlite3.IntegrityError as e:
        return "Integrity error: " + str(e), 400
    
def updateEvent(data_event, id_event, id_user):
    try :
        model.event.updateEvent(data_event, id_event, id_user)
        return "Event updated successfully", 200
    except sqlite3.IntegrityError as e:
        return "Integrity error: " + str(e), 400
    
def deleteEvent(id_event, id_user):
    try :
        model.event.deleteEvent(id_event, id_user)
        return "Event deleted successfully", 200
    except sqlite3.IntegrityError as e:
        return "Integrity error: " + str(e), 400

def getAllEvents() :
    try :
        events = model.event.getAllEvents()
        return {"events": events}, 200
    except sqlite3.IntegrityError as e:
        return {"error": "Integrity error: " + str(e)}, 500

def getAllNextEvents() :
    try :
        events = model.event.getAllNextEvents()
        return {"events": events}, 200
    except sqlite3.IntegrityError as e:
        return {"error": "Integrity error: " + str(e)}, 500

def getNextEvent(id_user) :
    try :
        events = model.event.getNextEvent(id_user)
        return {"events": events}, 200
    except sqlite3.IntegrityError as e:
        return {"error": "Integrity error: " + str(e)}, 500

def getMyEvents(id_user) :
    try :
        events = model.event.getMyEvents(id_user)
        return {"events": events}, 200
    except sqlite3.IntegrityError as e:
        return {"error": "Integrity error: " + str(e)}, 500