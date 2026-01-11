from typing import BinaryIO

import pandas as pd

from exceptions.exceptions import InvalidCsvFormat
from interfaces.repositories.student_repository_interface import IStudentRepository
from interfaces.resolver.github_client_resolver import IGitHubClientResolver
from interfaces.services.github_service_interface import IGitHubService


class GitHubService(IGitHubService):
    def __init__(
        self, student_repository: IStudentRepository, github_client_resolver: IGitHubClientResolver
    ):
        self._student_repo = student_repository
        self._gh_client_resolver = github_client_resolver

    def import_github_names(self, file: BinaryIO):
        df = pd.read_csv(file)

        required_columns = {"E-Mail-Adresse", "Texteingabe online"}
        if not required_columns.issubset(df.columns):
            raise InvalidCsvFormat

        for _, row in df.iterrows():
            email = str(row["E-Mail-Adresse"]).strip()
            text_submission = str(row["Texteingabe online"]).strip()

            if not email or email == "nan" or not text_submission or text_submission == "nan":
                continue

            student = self._student_repo.get_by_email(email)

            if not student:
                continue

            # submitted github name has not changed
            if student.github_username == text_submission:
                continue

            github_id = self._gh_client_resolver.get_user_id(text_submission)

            student.github_id = github_id
            student.github_username = text_submission

            self._student_repo.update(student.id, student)
