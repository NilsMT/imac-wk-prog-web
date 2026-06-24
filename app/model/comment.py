#import
from database import query_db

def getCommentsOnEvent(id_event):
    return query_db(
        """         
        SELECT u.firstname, u.name, u.pseudo, c.datetime, c.message 
        FROM COMMENT c, USER u 
        WHERE u.id_user = c.id_user AND c.id_event = ?           
        """,
        [id_event]
    )

def addComment(id_user,id_event,message,comment_time):
    return query_db("INSERT INTO COMMENT VALUES(?,?,?,?)",[id_user,id_event,message,comment_time])
