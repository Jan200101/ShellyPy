
class BadLogin(Exception):
    """
    Exception for bad login details
    """
    pass

class BadResponse(Exception):
    """
    Exception for bad responses from the target
    """
    pass

class NotFound(Exception):
    """
    Exception for 404 Not Found
    """
    pass
