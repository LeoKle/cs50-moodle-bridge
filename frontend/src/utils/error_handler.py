"""Global error handling utilities for the Streamlit application."""

import logging
from typing import NoReturn

import streamlit as st

from services.course_service import CourseServiceError

logger = logging.getLogger(__name__)


def handle_service_error(error: CourseServiceError, context: str = "operation") -> None:
    """Handle CourseServiceError with consistent messaging.

    Args:
        error: The CourseServiceError that occurred
        context: Context description for the error (e.g., "load courses", "create course")
    """
    logger.error("Service error during %s: %s", context, error)
    st.error(f"Failed to {context}: {error!s}")
    st.info("Make sure the backend is running and accessible.")


def handle_no_courses_available(redirect_page: str = "app.py") -> NoReturn:
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
