import io

import pytest

from exceptions.exceptions import InvalidCsvFormat
from models.student import StudentModel
from services.github_service import GitHubService
from tests.mocks.repositories.student_repository_mock import MockStudentRepository
from tests.mocks.resolvers.github_mock import MockGitHubClientResolver

pytestmark = pytest.mark.unit

CSV_HEADER = (
    'ID,"Vollständiger Name",E-Mail-Adresse,Status,Bewertung,Skala,'
    '"Bewertung kann geändert werden","Zuletzt geändert (Abgabe)",'
    '"Texteingabe online","Zuletzt geändert (Bewertung)",'
    '"Feedback als Kommentar"\n'
)

CSV_ROWS = (
    'Teilnehmer/in1234567,"Max Mustermann",max.mustermann@mail.de,'
    '"Zur Bewertung abgegeben - 36 Tage 10 Stunden zu spät -  - ",,'
    '"nicht bestanden    bestanden",Ja,'
    '"Dienstag, 2. Dezember 2025, 10:37","octocat   ",'
    '"Dienstag, 2. Dezember 2025, 10:37","This is feedback"\n'
    'Teilnehmer/in1234568,"Maxina Mustermann",maxina.mustermann@mail.de,'
    '"Zur Bewertung abgegeben - Bewertet -  - ",bestanden,'
    '"nicht bestanden    bestanden",Ja,'
    '"Dienstag, 2. Dezember 2025, 10:37","octocat   ",'
    '"Dienstag, 2. Dezember 2025, 10:37",\n'
    'Teilnehmer/in1234569,"Maximum Mustermann",maximum.mustermann@mail.de,'
    '"Zur Bewertung abgegeben - Verlängertes Abgabeende bis: Mittwoch, '
    '26. November 2025, 23:59 -  - ","nicht bestanden",'
    '"nicht bestanden    bestanden",Ja,'
    '"Dienstag, 2. Dezember 2025, 10:37","octocat   ",'
    '"Dienstag, 2. Dezember 2025, 10:37",\n'
)


@pytest.fixture
def github_service():
    student_repo = MockStudentRepository()
    github_client_resolver = MockGitHubClientResolver(users={"octocat": 1})
    gh_service = GitHubService(student_repo, github_client_resolver)

    return gh_service


def test_empty_csv(github_service):
    csv_content = (
        'ID,"Vollständiger Name",E-Mail-Adresse,Status,Bewertung,Skala,'
        '"Bewertung kann geändert werden","Zuletzt geändert (Abgabe)",'
        '"Texteingabe online","Zuletzt geändert (Bewertung)",'
        '"Feedback als Kommentar"\n'
    )
    csv_file = io.BytesIO(csv_content.encode())

    github_service.import_github_names(csv_file)


def test_import_updates_github_username_and_id(github_service):
    csv_file = io.BytesIO((CSV_HEADER + CSV_ROWS).encode())

    student = StudentModel(
        email="max.mustermann@mail.de",
        github_username=None,
        github_id=None,
    )
    github_service._student_repo.create(student)

    github_service.import_github_names(csv_file)

    updated = github_service._student_repo.get_by_email("max.mustermann@mail.de")

    assert updated is not None
    assert updated.github_username == "octocat"
    assert updated.github_id == 1


def test_import_skips_unknown_student(github_service):
    csv_content = CSV_HEADER + CSV_ROWS
    csv_file = io.BytesIO(csv_content.encode())

    github_service.import_github_names(csv_file)

    assert len(github_service._student_repo.get_all()) == 0


def test_import_skips_empty_github_name(github_service):
    csv_content = CSV_HEADER + 'Teilnehmer/in1,"Test User",test@mail.de,,,,,,"   ",,\n'
    csv_file = io.BytesIO(csv_content.encode())

    github_service._student_repo.create(
        StudentModel(
            email="test@mail.de",
            github_username=None,
            github_id=None,
        )
    )

    github_service.import_github_names(csv_file)

    student = github_service._student_repo.get_by_email("test@mail.de")
    assert student.github_username is None
    assert student.github_id is None


def test_import_skips_unchanged_github_name(github_service):
    csv_content = CSV_HEADER + CSV_ROWS
    csv_file = io.BytesIO(csv_content.encode())

    student = github_service._student_repo.create(
        StudentModel(
            email="max.mustermann@mail.de",
            github_username="octocat",
            github_id=1,
        )
    )

    github_service.import_github_names(csv_file)

    student = github_service._student_repo.get_by_email(student.email)


def test_import_raises_on_invalid_csv(github_service):
    csv_content = "email,github\nfoo@bar.com,octocat\n"
    csv_file = io.BytesIO(csv_content.encode())

    with pytest.raises(InvalidCsvFormat):
        github_service.import_github_names(csv_file)
