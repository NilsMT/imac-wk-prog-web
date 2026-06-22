#import
from database import query_db

def getAuthors():
    return query_db("SELECT * FROM EXEMPLE ex WHERE ex.ACTIVE = ?",[1])