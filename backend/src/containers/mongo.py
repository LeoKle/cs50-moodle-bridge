from dependency_injector import containers, providers
from pymongo import MongoClient

from repositories.mongo.course_repository import MongoCourseRepository


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
