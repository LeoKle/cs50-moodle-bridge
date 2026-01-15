"""Course UI components for the CS50 Moodle Bridge frontend."""

import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from interfaces.services.course_service_interface import CourseServiceInterface
from models.course import CourseCreate, CourseOut


def render_add_course_dialog(course_service: CourseServiceInterface) -> None:
    """Render dialog to add a new course."""
    if "show_add_dialog" not in st.session_state:
        st.session_state.show_add_dialog = False

    if st.button("➕ Add Course", type="primary", use_container_width=True):  # noqa: RUF001
        st.session_state.show_add_dialog = True

    if st.session_state.show_add_dialog:
        with st.form("add_course_form", clear_on_submit=True):
            st.subheader("Add New Course")

            course_name = st.text_input("Course Name*", placeholder="e.g., Introduction-to-CS")
            cs50_id = st.number_input(
                "CS50 ID (optional)",
                min_value=0,
                value=0,
                step=1,
            )

            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Create", type="primary", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("Cancel", use_container_width=True)

            if submit:
                if not course_name or not course_name.strip():
                    st.error("Course name is required")
                else:
                    try:
                        cs50_id_value = cs50_id if cs50_id > 0 else None
                        new_course = CourseCreate(name=course_name.strip(), cs50_id=cs50_id_value)
                        course_service.create_course(new_course)
                        st.success(f"Course '{course_name}' created successfully!")
                        st.session_state.show_add_dialog = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to create course: {e!s}")
                        raise
            if cancel:
                st.session_state.show_add_dialog = False
                st.rerun()


def render_course_list(courses: list[CourseOut]) -> None:
    """Render the list of courses."""
    if not courses:
        st.info("No courses available yet.")
        return

    if "expanded_course_id" not in st.session_state:
        st.session_state.expanded_course_id = None

    for course in courses:
        course_name = course.name or "Unnamed Course"
        course_id = course.id
        cs50_id = course.cs50_id
        exercise_ids = course.exercise_ids or []

        with stylable_container(
            key=f"course_{course_id}",
            css_styles="""
                {
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: 1rem;
                    margin-bottom: 1rem;
                    cursor: pointer;
                    transition: all 0.3s;
                }
                :hover {
                    border-color: rgba(49, 51, 63, 0.4);
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
            """,
        ):
            col1, col2, col3 = st.columns([0.05, 0.75, 0.2])

            with col1:
                st.markdown("📖")

            with col2:
                st.markdown(f"**{course_name}**")

                info_parts = []
                if cs50_id:
                    info_parts.append(f"CS50 ID: {cs50_id}")
                info_parts.append(f"{len(exercise_ids)} exercise(s)")
                st.caption(" • ".join(info_parts))

            with col3:
                is_expanded = st.session_state.expanded_course_id == course_id
                if st.button(
                    "Hide Details" if is_expanded else "View Details",
                    key=f"toggle_{course_id}",
                    use_container_width=True,
                    type="primary" if is_expanded else "secondary",
                ):
                    if is_expanded:
                        st.session_state.expanded_course_id = None
                    else:
                        st.session_state.expanded_course_id = course_id
                    st.rerun()

            if st.session_state.expanded_course_id == course_id:
                st.divider()

                detail_col1, detail_col2 = st.columns(2)

                with detail_col1:
                    st.markdown("##### 📋 Course Information")
                    st.markdown(f"**Course ID:** `{course_id}`")
                    st.markdown(f"**CS50 ID:** {cs50_id or '_Not linked_'}")
                    st.markdown(f"**Name:** {course_name}")

                with detail_col2:
                    st.markdown("##### 🎯 Exercises")
                    if exercise_ids:
                        st.markdown(f"**Total Exercises:** {len(exercise_ids)}")
                        with st.expander(f"View all {len(exercise_ids)} exercise IDs"):
                            for idx, ex_id in enumerate(exercise_ids, 1):
                                st.code(f"{idx}. {ex_id}", language=None)
                    else:
                        st.info("No exercises added yet")
