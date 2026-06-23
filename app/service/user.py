#import
import model.user

def registerUser(email,password,name,firstname,promo,pseudo):
    """
        Try to register a new user with the given infos

        Return:
        >>> 0 if success
        >>> 1 if user already exist
    """

    qr = model.user.registerUser(email,password,name,firstname,promo,pseudo)
    print(qr)
    return int(qr != 1) 

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