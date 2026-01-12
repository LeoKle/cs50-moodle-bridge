import streamlit as st

from services.course_service import CourseService, CourseServiceError
from ui.course_ui import render_add_course_dialog, render_course_list

st.set_page_config(
    page_title="CS50 Moodle Bridge",
    page_icon="📚",
    layout="wide",
)
course_service = CourseService()

st.title("📚 Courses")

render_add_course_dialog(course_service)

st.divider()

try:
    courses = course_service.get_courses()
    render_course_list(courses)
except CourseServiceError as e:
    st.error(f"Failed to load courses: {e!s}")
    st.info("Make sure the backend is running and accessible.")
