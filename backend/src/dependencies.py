import requests
from dependency_injector import containers, providers
from pymongo import MongoClient

from repositories.mongo.course_repository import MongoCourseRepository
from resolvers.github.auth import AnonymousGitHubAuth, GitHubAppAuth
from resolvers.github.client import GitHubClient
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

    github_session = providers.Singleton(requests.Session)

    github_auth = providers.Selector(
        config.github.use_auth,
        true=providers.Singleton(
            GitHubAppAuth,
            app_id=config.github.app_id,
            installation_id=config.github.installation_id,
            private_key_b64=config.github.private_key_base64,
            session=github_session,
        ),
        false=providers.Singleton(AnonymousGitHubAuth),
    )

    github_client = providers.Singleton(
        GitHubClient,
        auth=github_auth,
        session=github_session,
    )


if __name__ == "__main__":
    container = DependencyContainer()
    service = container.course_service()
    print(service)
