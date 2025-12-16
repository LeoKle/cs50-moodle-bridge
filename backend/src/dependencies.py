from dependency_injector import containers, providers
from pymongo import MongoClient

from repositories.mongo.course_repository import MongoCourseRepository
from services.course import CourseService
from settings import Settings


class DependencyContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_pydantic(Settings())

    mongo_client = providers.Singleton(
        MongoClient,
        config.mongo.uri,
    )

    mongo_database = providers.Singleton(
        lambda client, database: client[database],
        mongo_client,
        database=config.mongo.database,
    )

    course_collection = providers.Singleton(
        lambda db: db["courses"],
        mongo_database,
    )

    course_repository = providers.Singleton(
        MongoCourseRepository,
        collection=course_collection,
    )

    course_service = providers.Singleton(
        CourseService,
        course_repository=course_repository,
    )


if __name__ == "__main__":
    container = DependencyContainer()
    service = container.course_service()
    print(service)
