#import
import model.auth
import crypto

def tryToLogin(email,password):
    """
        Try to login user specified by `email` with given `password`

        Return:
        >>> 0 if success
        >>> 1 if wrong password
        >>> 2 if user doesnt exist
    """

    user = model.auth.getUserFromEmail(email)

    if user:
        is_valid = crypto.bcrypt.check_password_hash(
            user["password"],
            password
        )

        return int(not is_valid)
    else:
        return 2