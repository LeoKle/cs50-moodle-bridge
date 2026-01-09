"""Streamlit application for CS50 Moodle Bridge course management."""

import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import streamlit as st  # noqa: E402

from services.course_service import CourseService  # noqa: E402
from ui.course_ui import render_add_course_dialog, render_course_list  # noqa: E402

# Page configuration
st.set_page_config(
    page_title="CS50 Moodle Bridge",
    page_icon="📚",
    layout="wide",
)

# Initialize service
course_service = CourseService()

# Header
st.title("📚 Courses")

# Add course button
render_add_course_dialog(course_service)

st.divider()

# Course list
try:
    courses = course_service.get_courses()
    render_course_list(courses)
except Exception as e:  # noqa: BLE001
    st.error(f"Failed to load courses: {e!s}")
    st.info("Make sure the backend is running and accessible.")
