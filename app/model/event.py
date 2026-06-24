#import
from database import query_db, get_db
from utils import getCurrentTime

# SELECT
def getAllEvents():
    return query_db("SELECT *, COUNT(DISTINCT PARTICIPATION.id_user) AS nb_participants FROM EVENT JOIN ATTRIBUTE ON EVENT.id_event = ATTRIBUTE.id_event JOIN PARTICIPATION ON EVENT.id_event = PARTICIPATION.id_event GROUP BY EVENT.id_event")

def getAllNextEvents():
    return query_db("SELECT *, COUNT(DISTINCT PARTICIPATION.id_user) AS nb_participants FROM EVENT JOIN ATTRIBUTE ON EVENT.id_event = ATTRIBUTE.id_event JOIN PARTICIPATION ON EVENT.id_event = PARTICIPATION.id_event WHERE start_date > ? GROUP BY EVENT.id_event ORDER BY (start_date) ASC", [getCurrentTime()])

def getNextEvent(id_user):
    return query_db("SELECT *, COUNT(DISTINCT PARTICIPATION.id_user) AS nb_participants FROM EVENT JOIN ATTRIBUTE ON EVENT.id_event = ATTRIBUTE.id_event JOIN PARTICIPATION ON EVENT.id_event = PARTICIPATION.id_event WHERE start_date > ? AND PARTICIPATION.id_user == ? GROUP BY EVENT.id_event ORDER BY (start_date) ASC", [getCurrentTime(), id_user], True)

def getMyEvents(id_user):
    return query_db("SELECT *, COUNT(DISTINCT PARTICIPATION.id_user) AS nb_participants FROM EVENT JOIN ATTRIBUTE ON EVENT.id_event = ATTRIBUTE.id_event JOIN PARTICIPATION ON EVENT.id_event = PARTICIPATION.id_event WHERE EVENT.id_user = ? GROUP BY EVENT.id_event", [id_user])

# DELETE (only if the user is the owner of the event)
def deleteEvent(id_event, id_user):
    query_db("DELETE FROM EVENT WHERE id_event = ? AND id_user = ?", [id_event, id_user])
    query_db("DELETE FROM ATTRIBUTE WHERE id_event = ?", [id_event])

# INSERT
def insertEvent(data_event, id_user):
    col = ["name", "start_date", "end_date", "location", "id_user"]
    val = [data_event["name"], data_event["start_date"], data_event["end_date"], data_event["location"], id_user]

    if "image" in data_event:
        col.append("image")
        val.append(data_event["image"])

    if "description" in data_event:
        col.append("description")
        val.append(data_event["description"])

    query = "INSERT INTO EVENT (" + ", ".join(col) + ") VALUES (" + ", ".join(["?"] * len(val)) + ")"

    cursor =  get_db().cursor()
    cursor.execute(query, val)
    id_event = cursor.lastrowid

    if "attributes" in data_event:
        for attribute in data_event["attributes"]:
            att_query = "INSERT INTO ATTRIBUTE (id_event, type, name, value) VALUES (?, ?, ?, ?)"
            cursor.execute(att_query, (id_event, attribute["type"], attribute["name"], attribute["value"]))

    get_db().commit()
    return id_event

# UPDATE (only if the user is the owner of the event)
def updateEvent(data_event, id_event, id_user):
    updates = []
    values = []

    for key in ["name", "start_date", "end_date", "location", "image", "description"]:
        if key in data_event:
            updates.append(f"{key} = ?")
            values.append(data_event[key])

    query = "UPDATE EVENT SET " + ", ".join(updates) + " WHERE id_event = ? AND id_user = ?"
    values.extend([id_event, id_user])

    cursor = get_db().cursor()
    cursor.execute(query, values)

    cursor.execute("DELETE FROM ATTRIBUTE WHERE id_event = ?", (id_event,))

    if "attributes" in data_event:
        for attribute in data_event["attributes"]:
            att_query = "INSERT INTO ATTRIBUTE (id_event, type, name, value) VALUES (?, ?, ?, ?)"
            cursor.execute(att_query, (id_event, attribute["type"], attribute["name"], attribute["value"]))

    get_db().commit()
    return True