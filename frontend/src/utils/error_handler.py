"""Global error handling utilities for the Streamlit application."""

import logging
import time
from typing import NoReturn

import streamlit as st

import constants as const
from services.course_service import CourseService, CourseServiceError

logger = logging.getLogger(__name__)


def handle_error_service(
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


def handle_error_no_courses(redirect_page: str = "app.py") -> NoReturn:
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


def handle_error_backend_unavailable(redirect_page: str | None = None) -> NoReturn:
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


def handle_action_delete_course(
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
        time.sleep(const.DELETE_REDIRECT_DELAY)
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
