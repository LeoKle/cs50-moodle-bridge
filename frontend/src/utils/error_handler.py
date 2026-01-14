"""Global error handling utilities for the Streamlit application."""

import logging
import time
from functools import wraps
from typing import NoReturn

import streamlit as st

from services.course_service import CourseService, CourseServiceError

logger = logging.getLogger(__name__)


def handle_service_error(
    error: CourseServiceError, context: str = "operation", show_retry_hint: bool = True
) -> None:
    """Handle CourseServiceError

    Args:
        error: The CourseServiceError that occurred
        context: Context description for the error (e.g., "load courses", "create course")
    """
    logger.error("Service error during %s: %s", context, error)
    st.error(f"Failed to {context}: {error!s}")

    if show_retry_hint:
        st.info("Make sure the backend is running and accessible.")
        st.caption("💡 Try refreshing the page or checking your connection.")


def handle_no_courses_available(redirect_page: str = "home.py") -> NoReturn:
    """Handle the case when no courses are available.

    Args:
        redirect_page: The page to redirect to when the button is clicked

    Raises:
        st.stop: Always stops execution after displaying the message
    """
    st.warning("No courses available. Please create a course first.")
    if st.button("← Go to Courses", type="primary"):
        st.switch_page(redirect_page)
    st.stop()


def handle_backend_unavailable(redirect_page: str | None = None) -> NoReturn:
    """Handle backend unavailability with option to redirect.

    Args:
        redirect_page: Optional page to redirect to. If None, no redirect button is shown.

    Raises:
        st.stop: Always stops execution after displaying the message
    """
    st.error("Unable to connect to the backend service.")
    st.info("Make sure the backend is running and accessible.")

    if redirect_page and st.button("← Back to Courses", type="primary"):
        st.switch_page(redirect_page)

    st.stop()


def handle_delete_course(
    course_service: CourseService,
    course_id: str,
    course_name: str,
    redirect_page: str = "app.py",
) -> None:
    """Handle course deletion with success/error messaging and redirection."""
    try:
        course_service.delete_course(course_id)
        st.success(f"Course '{course_name}' has been successfully deleted!")
        st.info("Redirecting to home page...")
        time.sleep(1.5)
    except CourseServiceError as e:
        logger.exception("Failed to delete course %s", course_id)
        st.error(f"Failed to delete course: {e!s}")
        st.caption("Please try again or check the backend connection.")
        return
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException:
        logger.exception("Unexpected error deleting course %s", course_id)
        st.error("An unexpected error occurred. Please try again.")
        return

    st.switch_page(redirect_page)


def with_retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except CourseServiceError as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning("Retry attempt %d/%d failed", attempt + 1, max_attempts)
                    time.sleep(delay)
            if last_exception:
                raise last_exception

        return wrapper

    return decorator
