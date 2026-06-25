import model.event
import sqlite3

def createEvent(data_event, id_user, image_url):
    try:
        model.event.insertEvent(data_event, id_user, image_url)
        return "Event created successfully", None
    except sqlite3.IntegrityError as e:
        return None, "Integrity error: " + str(e)

def updateEvent(data_event, id_event, id_user):
    try:
        model.event.updateEvent(data_event, id_event, id_user)
        return "Event updated successfully", None
    except sqlite3.IntegrityError as e:
        return None, "Integrity error: " + str(e)

def deleteEvent(id_event, id_user):
    try:
        model.event.deleteEvent(id_event, id_user)
        return "Event deleted successfully", None
    except sqlite3.IntegrityError as e:
<<<<<<< HEAD
        return None, "Integrity error: " + str(e)
=======
        return "Integrity error: " + str(e), 400
    
def getEvent(id_event) :
    try :
        event = model.event.getEvent(id_event)

        if not event:
            return {}, 400
        
        event_dict = dict(event)
        attributes = model.event.getAttributes(event_dict["id_event"])
        attributes_list = [dict(attr) if hasattr(attr, 'keys') else attr for attr in attributes]
        event_dict["attributes"] = attributes_list
        
        return event_dict, 200
    except sqlite3.IntegrityError as e:
        return {"error": "Integrity error: " + str(e)}, 500
>>>>>>> e4caac1a9cd6ad54644f0d8673d5bf48175076e2

def getAllEvents():
    try:
        events = model.event.getAllEvents()
        if not events:
            return [], None
        result = []
        for event in events:
            event_dict = dict(event)
            attributes = model.event.getAttributes(event_dict["id_event"])
            event_dict["attributes"] = [dict(attr) if hasattr(attr, 'keys') else attr for attr in attributes]
            result.append(event_dict)
        return result, None
    except sqlite3.IntegrityError as e:
        return [], "Integrity error: " + str(e)

def getAllNextEvents():
    try:
        events = model.event.getAllNextEvents()
        if not events:
            return [], None
        result = []
        for event in events:
            event_dict = dict(event)
            attributes = model.event.getAttributes(event_dict["id_event"])
<<<<<<< HEAD
            event_dict["attributes"] = [dict(attr) if hasattr(attr, 'keys') else attr for attr in attributes]
            result.append(event_dict)
        return result, None
=======
            attributes_list = [dict(attr) if hasattr(attr, 'keys') else attr for attr in attributes]
            event_dict["attributes"] = attributes_list
            result.append(event_dict) 

        return result, 200
>>>>>>> e4caac1a9cd6ad54644f0d8673d5bf48175076e2
    except sqlite3.IntegrityError as e:
        return [], "Integrity error: " + str(e)

def getNextEvent(id_user):
    try:
        event = model.event.getNextEvent(id_user)
        if not event:
            return None, None
        event_dict = dict(event)
        attributes = model.event.getAttributes(event_dict["id_event"])
        event_dict["attributes"] = [dict(attr) if hasattr(attr, 'keys') else attr for attr in attributes]
        return event_dict, None
    except sqlite3.IntegrityError as e:
        return None, "Integrity error: " + str(e)

def getMyEvents(id_user):
    try:
        events = model.event.getMyEvents(id_user)
        if not events:
            return [], None
        result = []
        for event in events:
            event_dict = dict(event)
            attributes = model.event.getAttributes(event_dict["id_event"])
            event_dict["attributes"] = [dict(attr) if hasattr(attr, 'keys') else attr for attr in attributes]
            result.append(event_dict)
        return result, None
    except sqlite3.IntegrityError as e:
        return [], "Integrity error: " + str(e)
