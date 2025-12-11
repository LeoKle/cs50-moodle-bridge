from dependency_injector import containers, providers

from services.course import CourseService
from settings import Settings


class DependencyContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_pydantic(Settings())

    course_service = providers.Singleton(CourseService)


if __name__ == "__main__":
    container = DependencyContainer()
