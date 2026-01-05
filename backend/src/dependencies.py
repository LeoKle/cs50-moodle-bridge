import requests
from dependency_injector import containers, providers

from containers.mongo import MongoContainer
from resolvers.github.auth import AnonymousGitHubAuth, GitHubAppAuth
from resolvers.github.client import GitHubClient
from services.course import CourseService
from services.enrollment import EnrollmentService
from settings import Settings


class DependencyContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_pydantic(Settings())

    mongo = providers.Container(MongoContainer, config=config)

    course_service = providers.Singleton(
        CourseService,
        course_repository=mongo.course_repository,
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

    enrollment_service = providers.Singleton(
        EnrollmentService,
        student_repository=mongo.student_repository,
        course_repository=mongo.course_repository,
        enrollment_repository=mongo.enrollment_repository,
    )


if __name__ == "__main__":
    container = DependencyContainer()
    service = container.course_service()
    print(service)
