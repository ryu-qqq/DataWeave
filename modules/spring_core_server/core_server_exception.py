
class CoreServerException(Exception):
    """
       Core server exception for API response errors.
    """

    def __init__(self, message: str):
        super().__init__(message)

