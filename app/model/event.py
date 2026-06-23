#import
from database import query_db
from datetime import datetime

currentTime = datetime.now()

# Select
def getAllEvents():
    return query_db("SELECT * FROM EVENT")

def getAllNextEvents():
    return query_db("SELECT * FROM EVENT " \
    "WHERE start_date > ? " \
    "ORDER BY (start_date) ASC", [currentTime])

def getNextEvent(id_user):
    return query_db("SELECT * FROM EVENT E " \
    "JOIN PARTICIPATION P ON E.id_event = P.id_event " \
    "WHERE P.id_user = ? AND start_date > ? " \
    "ORDER BY (start_date) ASC", [id_user, currentTime], True)

# Verify if user is creator
def isCreator(id_user):
    return f"{id_user} == EVENT.id_user"

def getMyEvents(user):
    return query_db(f"SELECT * FROM EVENT WHERE {isCreator(user)}")

# Sorting
# JSON : {"sort_1" : none, ASS ou DESC, "sort_2" : none, ASC ou DESC,...}

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
# Delete event with boolean
def deleteEvent(user, id_row):
    return query_db(f"DELETE FROM EVENT E WHERE id_event = ? AND {isCreator(user)}", [id_row])

# Insert to create an event
# JSON : {"name" = ..., "start_date" = ...,..., "requis" = [{"entity" = ..., "attribute" = ..., "value" = ...}, {"entity" = ..., "attribute" = ..., "value" = ...}...]}

def insertEvent(name, start_date, end_date, location, image, description, requis, id_user):
    values = [name, start_date, end_date, location, id_user]
    query = "INSERT INTO EVENT VALUES(?,?,?,?,?"
    if (image is None and description is None and requis is None):
        return query_db(query + ")", values)
    else:
        if(image is not None):
            query += " ,?"
            values.append(image)
        if(description is not None):
            query += " ,?"
            values.append(description)
        if(requis is not None):
            query += " ,?"
            values.append(requis)
        return query_db(query + ")")
    
# Update an event