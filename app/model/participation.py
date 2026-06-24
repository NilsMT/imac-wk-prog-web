#import
from database import query_db

def addParticipation(id_user,id_event):
    return query_db("INSERT INTO PARTICIPATION VALUES(?,?)",[id_user,id_event])

def removeParticipation(id_user,id_event):
    return query_db("DELETE FROM PARTICIPATION WHERE id_user = ? AND id_event = ?",[id_user,id_event])