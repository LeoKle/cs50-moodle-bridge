"""Dependency injection container configuration."""

import os

from dependency_injector import containers, providers

from interfaces.services import CourseServiceInterface
from interfaces.services.enrollment_service_interface import EnrollmentServiceInterface


class Container(containers.DeclarativeContainer):
    """
    Dependency injection container for the frontend application.

    This container manages the instantiation and lifecycle of services,
    enabling clean separation between production and mock implementations.
    The mode is automatically determined from the USE_MOCK_SERVICES environment variable.
    """

    config = providers.Configuration()

    course_service: providers.Provider[CourseServiceInterface] = providers.Selector(
        config.mode,
        production=providers.Factory(
            lambda: __import__(
                "services.course_service", fromlist=["CourseService"]
            ).CourseService()
        ),
        mock=providers.Factory(
            lambda: __import__(
                "services.mock_course_service", fromlist=["MockCourseService"]
            ).MockCourseService()
        ),
    )

    enrollment_service: providers.Provider[EnrollmentServiceInterface] = providers.Selector(
        config.mode,
        production=providers.Factory(
            lambda: __import__(
                "services.enrollment_service", fromlist=["EnrollmentService"]
            ).EnrollmentService()
        ),
        mock=providers.Factory(
            lambda: __import__(
                "services.mock_enrollment_service", fromlist=["MockEnrollmentService"]
            ).MockEnrollmentService()
        ),
    )


# Create and configure the application container singleton
container = Container()
_mode = "mock" if os.getenv("USE_MOCK_SERVICES", "false").lower() == "true" else "production"
container.config.mode.from_value(_mode)
