class TransformError(BaseException):
    """Raised when a valid transformation between input and output CRS cannot be found"""


class ZConversionWarning(UserWarning):
    """Raised to alert user that z values were input but not changed."""
