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

def updateUser(email, password, name, firstname, promo, pseudo, id_user):
    updates = []
    params = []

    if name is not None:
        updates.append("name=?")
        params.append(name)
    if firstname is not None:
        updates.append("firstname=?")
        params.append(firstname)
    if email is not None:
        updates.append("email=?")
        params.append(email)
    if pseudo is not None:
        updates.append("pseudo=?")
        params.append(pseudo)
    if promo is not None:
        updates.append("promo=?")
        params.append(promo)
    if password is not None:
        updates.append("password=?")
        params.append(crypto.bcrypt.generate_password_hash(password, 10))

    if not updates:
        return 0

    params.append(id_user)
    query = f"UPDATE USER SET {', '.join(updates)} WHERE id_user=?"
    return query_db(query, params)

def updatePassword(password, id_user):
    password_hash = crypto.bcrypt.generate_password_hash(password, 10)
    return query_db("UPDATE USER SET password=? WHERE id_user=?", [password_hash, id_user])

def deleteUser(email):
    return query_db("DELETE FROM USER WHERE email=?",[email])