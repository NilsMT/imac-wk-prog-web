#import
from database import query_db
import crypto
import uuid

def registerUser(email,password,name,firstname,promo,pseudo):
    admin = 0
    active = 1
    id_user = str(uuid.uuid4())
    password = crypto.bcrypt.generate_password_hash(password, 10)

    return query_db("INSERT INTO USER VALUES(?,?,?,?,?,?,?,?,?)",[id_user,name,firstname,email,pseudo,promo,password,admin,active])

def deleteUser(email):
    return query_db("DELETE FROM USER WHERE email=?",[email])