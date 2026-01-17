"""Dependency injection container - matches backend architecture pattern."""

from dependency_injector import containers, providers

from config.settings import get_app_settings
from interfaces.repositories.course_repository_interface import (
    CourseRepositoryInterface,
)
from interfaces.repositories.enrollment_repository_interface import (
    EnrollmentRepositoryInterface,
)
from interfaces.services import CourseServiceInterface
from interfaces.services.enrollment_service_interface import EnrollmentServiceInterface


class DependencyContainer(containers.DeclarativeContainer):
    """
    Main DI container.

    Configuration is automatically determined from environment variables:
    - USE_MOCK_SERVICES=true: Use mock implementations for standalone development
    - USE_MOCK_SERVICES=false: Use production implementations calling backend API
    """

    config = providers.Configuration()

    course_repository: providers.Provider[CourseRepositoryInterface] = providers.Selector(
        config.mode,
        production=providers.Singleton(
            lambda: __import__(
                "repositories.course_repository", fromlist=["CourseRepository"]
            ).CourseRepository()
        ),
        mock=providers.Singleton(
            lambda: __import__(
                "mocks.repositories.course_repository_mock",
                fromlist=["MockCourseRepository"],
            ).MockCourseRepository()
        ),
    )

    enrollment_repository: providers.Provider[EnrollmentRepositoryInterface] = providers.Selector(
        config.mode,
        production=providers.Singleton(
            lambda: __import__(
                "repositories.enrollment_repository",
                fromlist=["EnrollmentRepository"],
            ).EnrollmentRepository()
        ),
        mock=providers.Singleton(
            lambda: __import__(
                "mocks.repositories.enrollment_repository_mock",
                fromlist=["MockEnrollmentRepository"],
            ).MockEnrollmentRepository()
        ),
    )

    course_service: providers.Provider[CourseServiceInterface] = providers.Singleton(
        lambda repo: __import__(
            "services.course_service", fromlist=["CourseService"]
        ).CourseService(repository=repo),
        repo=course_repository,
    )

    enrollment_service: providers.Provider[EnrollmentServiceInterface] = providers.Singleton(
        lambda repo: __import__(
            "services.enrollment_service", fromlist=["EnrollmentService"]
        ).EnrollmentService(repository=repo),
        repo=enrollment_repository,
    )


container = DependencyContainer()

_settings = get_app_settings()
_mode = "mock" if _settings.use_mock_services else "production"
container.config.mode.from_value(_mode)
