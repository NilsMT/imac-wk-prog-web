#import
from database import query_db

def getUserFromEmail(email):
    return query_db("SELECT * FROM USER u WHERE u.email = ?",[email],one=True)