import model.event
import sqlite3

def createEvent(data_event, id_user, image_url):
    try :
        model.event.insertEvent(data_event, id_user, image_url)
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

        if not events:
            return [], 200
        
        result = []
        for event in events:
            event_dict = dict(event)
            attributes = model.event.getAttributes(event_dict["id_event"])
            attributes_list = [dict(attr) if hasattr(attr, 'keys') else attr for attr in attributes]
            event_dict["attributes"] = attributes_list
            result.append(event_dict)

        return result, 200
    except sqlite3.IntegrityError as e:
        return {"error": "Integrity error: " + str(e)}, 500

def getAllNextEvents() :
    try :
        events = model.event.getAllNextEvents()

        if not events:
            return [], 200
        
        result = []
        for event in events:
            event_dict = dict(event)
            attributes = model.event.getAttributes(event_dict["id_event"])
            attributes_list = [dict(attr) if hasattr(attr, 'keys') else attr for attr in attributes]
            event_dict["attributes"] = attributes_list
            result.append(event_dict)

        print("Result:", result)  # Debugging line to print the result  

        return result, 200
    except sqlite3.IntegrityError as e:
        return {"error": "Integrity error: " + str(e)}, 500

def getNextEvent(id_user) :
    try :
        event = model.event.getNextEvent(id_user)

        if not event:
            return {}, 200
        
        event_dict = dict(event)
        attributes = model.event.getAttributes(event_dict["id_event"])
        attributes_list = [dict(attr) if hasattr(attr, 'keys') else attr for attr in attributes]
        event_dict["attributes"] = attributes_list
        
        return event_dict, 200
    except sqlite3.IntegrityError as e:
        return {"error": "Integrity error: " + str(e)}, 500

def getMyEvents(id_user) :
    try :
        events = model.event.getMyEvents(id_user)
        
        if not events:
            return [], 200
        
        result = []
        for event in events:
            event_dict = dict(event)
            attributes = model.event.getAttributes(event_dict["id_event"])
            attributes_list = [dict(attr) if hasattr(attr, 'keys') else attr for attr in attributes]
            event_dict["attributes"] = attributes_list
            result.append(event_dict)

        return result, 200
    except sqlite3.IntegrityError as e:
        return {"error": "Integrity error: " + str(e)}, 500