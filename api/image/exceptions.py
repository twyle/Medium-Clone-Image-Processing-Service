class EmptyImageFile(Exception):
    """Raised when no image file is given."""


class IllegalFileType(Exception):
    """Raised when an illegal file type is uploaded."""
    
class UserDoesNotExist(Exception):
    """Raised when the given user does not exist."""
    
class InvalidEmailAddressFormat(Exception):
    """Raised when the email address format is invalid."""