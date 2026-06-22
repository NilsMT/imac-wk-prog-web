#import
from database import query_db

def getAuthors():
    return query_db("SELECT * FROM Author a WHERE a.active = ?",[1])