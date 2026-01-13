from dependency_injector import containers, providers
from pymongo import MongoClient

from repositories.mongo.course_repository import MongoCourseRepository
from repositories.mongo.cs50_submission_problem_repository import (
    MongoSubmissionProblemRepository,
)
from repositories.mongo.enrollment_repository import MongoEnrollmentRepository
from repositories.mongo.migration import (
    init_cs50_submission_problem_collection,
    init_enrollment_collection,
    init_student_collection,
)
from repositories.mongo.student_repository import MongoStudentRepository


class MongoContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    mongo_client = providers.Singleton(
        MongoClient,
        config.mongo.uri,
    )

    mongo_database = providers.Singleton(
        lambda client, name: client[name],
        mongo_client,
        name=config.mongo.database,
    )

    course_collection = providers.Singleton(
        lambda db: db["courses"],
        mongo_database,
    )

    course_repository = providers.Singleton(
        MongoCourseRepository,
        collection=course_collection,
    )

    student_collection = providers.Singleton(
        lambda db: db["students"],
        mongo_database,
    )

    student_collection_init = providers.Resource(
        init_student_collection,
        collection=student_collection,
    )

    student_repository = providers.Singleton(
        MongoStudentRepository,
        collection=student_collection,
    )

    enrollment_collection = providers.Singleton(
        lambda db: db["enrollments"],
        mongo_database,
    )

    enrollment_collection_init = providers.Resource(
        init_enrollment_collection,
        collection=enrollment_collection,
    )

    enrollment_repository = providers.Singleton(
        MongoEnrollmentRepository, collection=enrollment_collection
    )

    cs50_submission_problem_collection = providers.Singleton(
        lambda db: db["cs50_submissions"],
        mongo_database,
    )

    cs50_submission_problem_collection_init = providers.Resource(
        init_cs50_submission_problem_collection,
        collection=cs50_submission_problem_collection,
    )

    cs50_submission_problem_repository = providers.Singleton(
        MongoSubmissionProblemRepository,
        collection=cs50_submission_problem_collection,
    )
