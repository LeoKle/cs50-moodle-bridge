from pymongo.collection import Collection

from interfaces.repositories.cs50_submission_problem_repository_interface import (
    ICS50SubmissionProblemRepository,
)
from models.cs50_submission_problem import CS50SubmissionProblemModel


class MongoSubmissionProblemRepository(ICS50SubmissionProblemRepository):
    def __init__(self, collection: Collection):
        self._collection = collection

    def upload_submissions(self, submission_problem: CS50SubmissionProblemModel):
        document = submission_problem.model_dump()

        self._collection.update_one(
            {"slug": submission_problem.slug},
            {"$set": document},
            upsert=True,
        )

    def get_submissions(self, slug: str) -> CS50SubmissionProblemModel | None:
        doc = self._collection.find_one({"slug": slug})
        if not doc:
            return None

        doc.pop("_id", None)
        return CS50SubmissionProblemModel(**doc)
