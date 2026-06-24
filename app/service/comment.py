#import
import model.comment

def getCommentsOnEvent(id_event):
    """
        Give the list of comments and user data associated to it for a given event
        Return:
        >>> the list of comment+user data for the event, or [] if none/failure.
    """
    return model.comment.getCommentsOnEvent(id_event)

def addComment(id_user,id_event,message,comment_time):
    """
        Try to register a new user with the given infos

        Return:
        >>> 0 if success
        >>> 1 if failure
    """
    qr = model.comment.addComment(id_user,id_event,message,comment_time)
    return 0 if qr == 1 else 1