#import
import model.user
import sqlite3

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
    return int(qr != 1)