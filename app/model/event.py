#import
from database import query_db
from datetime import datetime
# Found on : https://pytutorial.com/python-datetime-to-string-guide/
def getCurrentTime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# SELECT
def getAllEvents():
    return query_db("SELECT * FROM EVENT")

def getAllNextEvents():
    return query_db("SELECT * FROM EVENT WHERE start_date > ? ORDER BY (start_date) ASC", [getCurrentTime()])

def getNextEvent(id_user):
    return query_db("SELECT * FROM EVENT E JOIN PARTICIPATION P ON E.id_event = P.id_event WHERE P.id_user = ? AND start_date > ? ORDER BY (start_date) ASC", [id_user, getCurrentTime()], True)

# Verify if user is creator
def getMyEvents(id_user):
    return query_db("SELECT * FROM EVENT WHERE EVENT.id_user = ?", [id_user])

# SORING
# JSON : {"sort_1" : None, ASS ou DESC, "sort_2" : None, ASC ou DESC,...}

def getEventsSorted(name, start_date, end_date, location):
    query = "SELECT * FROM EVENT"
    if (name is None and start_date is None and end_date is None and location is None):
        return query_db(query)
    else:
        query += " ORDER BY"

        if(name is not None):
            query += " name " + name + ","
        if(start_date is not None):
            query += " start_date " + start_date + ","
        if(end_date is not None):
            query += " end_date " + end_date + ","
        if(location is not None):
            query += " location " + location + ","
    # Cut last ","
    query = query[0:-1]
    return query_db(query)

# Only if user is creator
# DELETE event
def deleteEvent(id_user, id_row):
    return query_db("DELETE FROM EVENT WHERE id_event = ? AND id_user = ?", [id_row, id_user])

# INSERT to create an event
# JSON : {"name" = ..., "start_date" = ...,..., "requis" = [{"entity" = ..., "attribute" = ..., "value" = ...}, {"entity" = ..., "attribute" = ..., "value" = ...}...]}

def insertEvent(name, start_date, end_date, location, image, description, requis, id_user):
    # Same way as sorting
    query_begin = "INSERT INTO EVENT (name, start_date, end_date, location, id_user"
    query_end = ") VALUES (?,?,?,?,?"
    values = [name, start_date, end_date, location, id_user]

    if(image is not None):
        query_begin += ", image"
        query_end += ',?'
        values.append(image)

    if(description is not None):
        query_begin += ", description"
        query_end += ',?'
        values.append(description)

    # We create the event
    query_db(query_begin + query_end + ")", values, True)
    # For INSERT, query_db returns nb of rows affected (!= row like in SELECT)
    # For ENTITY, we need the id_event : we use SELECT to get the row
    id_event = query_db("SELECT id_event FROM EVENT WHERE name = ? AND start_date = ? AND id_user = ?", [name, start_date, id_user], True)["id_event"]
    
    if (requis is not None):
        for eav in requis:
            entity_type, attribut, value = eav["entity"], eav["attribute"], eav["value"]
            # We create the entity
            query_db("INSERT INTO ENTITY (type, id_event) VALUES (?,?)", [entity_type, id_event], True)
            # To create the value, we need the entity id that we get from the row
            id_entity = query_db("SELECT id_entity FROM ENTITY WHERE type = ? AND id_event = ?", [entity_type, id_event], True)["id_entity"]
            # We create the value
            query_db("INSERT INTO VALUE(id_attribut, id_entity, value) VALUES (?,?,?)", [attribut, id_entity, value])
    return id_event

# UPDATE an event : everything is updated, even if no changes
def updateEvent(name, start_date, end_date, location, image, description, requis, id_row):
    query_db("UPDATE EVENT SET name = ?, start_date = ?, end_date = ?, location = ?, image = ?, description = ? WHERE id_event = ?", [name, start_date, end_date, location, image, description, id_row])
    # Same as INSERT
    id_event = id_row
    if (requis is not None):
        for eav in requis:
            entity_type, attribut, value = eav["entity"], eav["attribute"], eav["value"]
            # We create the entity
            query_db("INSERT INTO ENTITY (type, id_event) VALUES (?,?)", [entity_type, id_event], True)
            # To create the value, we need the entity id
            id_entity = query_db("SELECT id_entity FROM ENTITY WHERE type = ? AND id_event = ?", [entity_type, id_event])
            # We create the value
            query_db("INSERT INTO VALUE(id_attribut, id_entity, value) VALUES (?,?,?)", [attribut, id_entity, value])
    return id_event