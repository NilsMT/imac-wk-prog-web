#import
from database import query_db

def getUsers():
    return query_db("SELECT id_user, name, firstname, email, pseudo, promo, admin, active FROM USER")

def setActive(id_user, active):
    return query_db("UPDATE USER SET active = ? WHERE id_user = ?", [active, id_user])

def setAdmin(id_user, admin):
    return query_db("UPDATE USER SET admin = ? WHERE id_user = ?", [admin, id_user])