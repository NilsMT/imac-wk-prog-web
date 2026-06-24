#import
import model.admin

def getUsers():
    """
        Get all users (without password)

        Return:
        >>> [...] list of users
    """
    return model.admin.getUsers()

def setActive(id_user, active):
    """
        Set a user's active status

        Return:
        >>> 0 if success
        >>> 1 if user not found
    """
    qr = model.admin.setActive(id_user, active)
    return 0 if qr == 1 else 1

def setAdmin(id_user, admin):
    """
        Set a user's admin status

        Return:
        >>> 0 if success
        >>> 1 if user not found
    """
    qr = model.admin.setAdmin(id_user, admin)
    return 0 if qr == 1 else 1