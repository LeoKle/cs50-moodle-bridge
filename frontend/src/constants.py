"""Constants for the CS50 Moodle Bridge frontend application."""

# API Configuration
DEFAULT_BACKEND_URL = "http://localhost:8000"
API_V1_PREFIX = "/api/v1"
COURSES_ENDPOINT = "/courses"
REQUEST_TIMEOUT = 30

# Page Routes
HOME_PAGE = "app.py"
COURSE_DETAIL_PAGE = "pages/course_detail.py"

# UI Labels
BUTTON_ADD_COURSE = "➕ Add Course"  # noqa: RUF001
BUTTON_BACK = "← Back"
BUTTON_GO_TO_COURSES = "← Go to Courses"
BUTTON_BACK_TO_COURSES = "← Back to Courses"
BUTTON_VIEW_DETAILS = "View Details"
BUTTON_HIDE_DETAILS = "Hide Details"
BUTTON_CREATE = "Create"
BUTTON_CANCEL = "Cancel"
BUTTON_UPDATE_COURSE = "💾 Update Course"
BUTTON_REFRESH = "🔄 Refresh"
BUTTON_DELETE_COURSE = "🗑️ Delete Course"
BUTTON_COPY_EXERCISE_IDS = "📋 Copy All Exercise IDs"

# UI Messages
MESSAGE_NO_COURSES = "No courses available yet."
MESSAGE_NO_EXERCISES = "No exercises have been added to this course yet."
MESSAGE_BACKEND_UNAVAILABLE = "Unable to connect to the backend service."
MESSAGE_BACKEND_CHECK = "Make sure the backend is running and accessible."
MESSAGE_COURSE_NAME_REQUIRED = "Course name is required"
MESSAGE_UPDATE_COMING_SOON = "Update functionality coming soon!"
MESSAGE_UPDATE_FEATURE_DESCRIPTION = "This feature will allow you to modify course details."
MESSAGE_REDIRECTING = "Redirecting to home page..."
MESSAGE_EXERCISE_IDS_COPIED = "Exercise IDs displayed above - copy them from the code block"
MESSAGE_SELECT_COURSE = "Please select a course from the dropdown above."

# UI Icons
ICON_BOOK = "📖"
ICON_BOOKS = "📚"
ICON_TARGET = "🎯"
ICON_SETTINGS = "⚙️"
ICON_INFO = "📋"

# Form Field Placeholders
PLACEHOLDER_COURSE_NAME = "e.g., Introduction-to-CS"

# Validation
MIN_COURSE_NAME_LENGTH = 1
MIN_CS50_ID = 0
DEFAULT_CS50_ID = 0

# Retry Configuration
DEFAULT_MAX_RETRY_ATTEMPTS = 3
DEFAULT_RETRY_DELAY = 1.0

# Time Configuration
DELETE_REDIRECT_DELAY = 1.5
