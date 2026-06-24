#import
import model.participation
import sqlite3

def addParticipation(id_user, id_event):
    """
        Try to register a new user with the given infos

        Return:
        >>> 0 if success
        >>> 1 if participation already exists
        >>> 2 unknown error
    """
    try:
        qr = model.participation.addParticipation(id_user, id_event)
        return 0 if qr == 1 else 2
    except sqlite3.IntegrityError:
        return 1

def removeParticipation(id_user, id_event):
    """
        Try to remove a participation

        Return:
        >>> 0 if success
        >>> 1 if participation didn't exist
    """
    qr = model.participation.removeParticipation(id_user, id_event)

    return 0 if qr == 1 else 1