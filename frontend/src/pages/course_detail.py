"""Course detail page for viewing and managing individual courses."""

import streamlit as st

import constants as const
from services.course_service import CourseService, CourseServiceError
from utils import error_handler

st.set_page_config(
    page_title="Course Details - CS50 Moodle Bridge",
    page_icon="📖",
    layout="wide",
)

course_service = CourseService()

st.title("📖 Course Details")

try:
    all_courses = course_service.get_courses()
except CourseServiceError as e:
    error_handler.handle_service_error(e, "load courses")
    st.stop()

if not all_courses:
    error_handler.handle_no_courses_available()

course_options = {f"{course.name} (...{course.id[-4:]})": course.id for course in all_courses}
course_display_names = list(course_options.keys())

selected_course_display = st.selectbox(
    "Select a course to view details:",
    options=course_display_names,
    index=0 if course_display_names else None,
    help="Choose a course from the dropdown to view its details",
)

course_id = course_options[selected_course_display] if selected_course_display else None

if not course_id:
    st.info(const.MESSAGE_SELECT_COURSE)
    st.stop()

try:
    course = course_service.get_course(course_id)

    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        st.header(course.name)
    with col2:
        if st.button(const.BUTTON_BACK, use_container_width=True):
            st.switch_page(const.HOME_PAGE)

    st.divider()

    tab1, tab2, tab3 = st.tabs([
        f"{const.ICON_INFO} Overview",
        f"{const.ICON_TARGET} Exercises",
        f"{const.ICON_SETTINGS} Settings",
    ])

    with tab1:
        st.subheader("Course Overview")

        info_col1, info_col2, info_col3 = st.columns(3)

        with info_col1:
            st.metric(label="Course ID", value=course.id, help="MongoDB Object ID")

        with info_col2:
            st.metric(
                label="CS50 ID",
                value=course.cs50_id or "Not linked",
                help="CS50 course identifier",
            )

        with info_col3:
            st.metric(
                label="Total Exercises",
                value=len(course.exercise_ids),
                help="Number of exercises in this course",
            )

        st.divider()

        st.subheader("Course Details")

        details_col1, details_col2 = st.columns(2)

        with details_col1:
            st.markdown("**Course Name:**")
            st.info(course.name)

            st.markdown("**Course ID:**")
            st.code(course.id, language=None)

        with details_col2:
            st.markdown("**CS50 Integration:**")
            if course.cs50_id:
                st.success(f"Linked to CS50 Course ID: {course.cs50_id}")
            else:
                st.warning("Not linked to CS50")

            st.markdown("**Exercise Count:**")
            st.info(f"{len(course.exercise_ids)} exercise(s) configured")

    with tab2:
        st.subheader("Exercises")

        if course.exercise_ids:
            st.write(f"This course has **{len(course.exercise_ids)}** exercise(s):")

            for idx, exercise_id in enumerate(course.exercise_ids, 1):
                with st.container():
                    ex_col1, ex_col2 = st.columns([0.1, 0.9])
                    with ex_col1:
                        st.markdown(f"**{idx}.**")
                    with ex_col2:
                        st.code(exercise_id, language=None)

            st.divider()

            if st.button(const.BUTTON_COPY_EXERCISE_IDS, use_container_width=True):
                exercise_list = "\n".join(course.exercise_ids)
                st.code(exercise_list, language=None)
                st.success(const.MESSAGE_EXERCISE_IDS_COPIED)
        else:
            st.info(const.MESSAGE_NO_EXERCISES)
            st.markdown("""
            **To add exercises:**
            - Use the API to add exercise IDs to this course
            - Or update the course configuration through the backend
            """)

    with tab3:
        st.subheader("Course Settings")

        st.markdown("### Course Information")

        with st.form("course_settings_form"):
            course_name_input = st.text_input(
                "Course Name",
                value=course.name,
                help="The display name for this course",
            )

            cs50_id_input = st.number_input(
                "CS50 Course ID",
                value=course.cs50_id or 0,
                min_value=0,
                step=1,
                help="Link this course to a CS50 course ID (0 = not linked)",
            )

            st.divider()

            col1, col2, col3 = st.columns(3)

            with col1:
                update_button = st.form_submit_button(
                    const.BUTTON_UPDATE_COURSE, type="primary", use_container_width=True
                )

            with col2:
                refresh_button = st.form_submit_button(
                    const.BUTTON_REFRESH, use_container_width=True
                )

            with col3:
                delete_button = st.form_submit_button(
                    const.BUTTON_DELETE_COURSE, use_container_width=True
                )

            if update_button:
                st.info(const.MESSAGE_UPDATE_COMING_SOON)
                st.caption(const.MESSAGE_UPDATE_FEATURE_DESCRIPTION)

            if refresh_button:
                st.rerun()

            if delete_button:
                error_handler.handle_delete_course(course_service, course_id, course.name)

        st.divider()

        st.markdown("### Advanced")
        with st.expander("📊 Raw Course Data (JSON)"):
            st.json(course.model_dump(mode="json"))

except CourseServiceError as e:
    error_handler.handle_service_error(e, "load course")
    error_handler.handle_backend_unavailable(redirect_page=const.HOME_PAGE)
