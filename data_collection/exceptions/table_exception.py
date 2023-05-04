class InsufficientTableException(Exception):
    """Exception raised when less than 2 table elements are found.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super().__init__(message)
