#import
import model.user
import sqlite3

def updateUser(email, password, name, firstname, promo, pseudo, id_user):
    """
        Try to update user info with partial data

        Return:
        >>> 0 if success
        >>> 1 if user mail taken already
        >>> 2 if user pseudo taken already
    """
    try:
        model.user.updateUser(email, password, name, firstname, promo, pseudo, id_user)
        return 0
    except sqlite3.IntegrityError as e:
        if "USER.email" in str(e):
            return 1
        if "USER.pseudo" in str(e):
            return 2
        raise

def updatePassword(password, id_user):
    """
        Try to update user password

        Return:
        >>> 0 if success
    """
    try:
        model.user.updatePassword(password, id_user)
        return 0
    except Exception as e:
        raise

def registerUser(email,password,name,firstname,promo,pseudo):
    """
        Try to register a new user with the given infos

        Return:
        >>> 0 if success
        >>> 1 if user mail taken already
        >>> 2 if user pseudo taken already
    """
    try:
        model.user.registerUser(email,password,name,firstname,promo,pseudo)
        return 0
    except sqlite3.IntegrityError as e:
        if "USER.email" in str(e):
            return 1
        if "USER.pseudo" in str(e):
            return 2
        raise

def deleteUser(email):
    """
        Try to delete a user with the given `email`

        Return:
        >>> 0 if success
        >>> 1 if user doesnt exist
    """

    qr = model.user.deleteUser(email)
    print(qr)
    return 0 if qr == 1 else 1