class CourseDoesNotExistException(Exception): ...


class InvalidCsvFormat(Exception):
    """Raised when the CSV format is not recognized"""


class InvalidJsonFormat(Exception):
    """Raised when the JSON format is not recognized"""
