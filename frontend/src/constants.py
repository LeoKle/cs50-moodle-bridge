"""Constants for the CS50 Moodle Bridge frontend application."""

# API Configuration
DEFAULT_BACKEND_URL = "http://localhost:8000"
API_V1_PREFIX = "/api/v1"
COURSES_ENDPOINT = "/courses"
ENROLLMENT_ENDPOINT = "/enroll"
REQUEST_TIMEOUT = 30

# Validation
MIN_COURSE_NAME_LENGTH = 1
MIN_CS50_ID = 0
DEFAULT_CS50_ID = 0

# Retry Configuration
DEFAULT_MAX_RETRY_ATTEMPTS = 3
DEFAULT_RETRY_DELAY = 1.0

# Time Configuration
DELETE_REDIRECT_DELAY = 1.5
