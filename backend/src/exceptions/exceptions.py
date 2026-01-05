class CourseDoesNotExistException(Exception): ...


class InvalidCsvFormat(Exception):
    """Raised when the CSV format is not recognized"""
