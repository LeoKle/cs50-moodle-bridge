from dependency_injector import containers, providers

from containers.mongo import MongoContainer
from services.course import CourseService
from settings import Settings


class DependencyContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_pydantic(Settings())

    mongo = providers.Container(MongoContainer, config=config)

    course_service = providers.Singleton(
        CourseService,
        course_repository=mongo.course_repository,
    )


if __name__ == "__main__":
    container = DependencyContainer()
    service = container.course_service()
    print(service)
