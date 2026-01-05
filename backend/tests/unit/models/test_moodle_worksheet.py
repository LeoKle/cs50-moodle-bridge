from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from models.moodle_worksheet import GradeType, MoodleWorksheetRowModel, PassFailGrade

pytestmark = pytest.mark.unit


def default_valid_model():
    """Common valid default base model."""
    return {
        "submission_id": "sub-123",
        "email": "student@example.com",
        "status": "graded",
        "grade_scale": "0-100",
        "submission_last_modified": datetime.now(UTC),
        "grade_last_modified": datetime.now(UTC),
        "feedback_comment": "Well done",
    }


def test_numeric_grade_valid():
    worksheet = MoodleWorksheetRowModel(
        **default_valid_model(),
        grade_type=GradeType.numeric,
        grade_numeric=87.5,
    )

    assert worksheet.grade_numeric == 87.5
    assert worksheet.grade_pass_fail is None


def test_pass_fail_grade_valid():
    worksheet = MoodleWorksheetRowModel(
        **default_valid_model(),
        grade_type=GradeType.pass_fail,
        grade_pass_fail=PassFailGrade.passed,
    )

    assert worksheet.grade_pass_fail == PassFailGrade.passed
    assert worksheet.grade_numeric is None


def test_numeric_grade_with_pass_fail_fails():
    with pytest.raises(ValidationError) as exc:
        MoodleWorksheetRowModel(
            **default_valid_model(),
            grade_type=GradeType.numeric,
            grade_numeric=90.0,
            grade_pass_fail=PassFailGrade.passed,
        )

    assert "Numeric grade requires grade_numeric only" in str(exc.value)


def test_numeric_grade_missing_numeric_value_fails():
    with pytest.raises(ValidationError) as exc:
        MoodleWorksheetRowModel(
            **default_valid_model(),
            grade_type=GradeType.numeric,
        )

    assert "Numeric grade requires grade_numeric only" in str(exc.value)


def test_pass_fail_grade_with_numeric_fails():
    with pytest.raises(ValidationError) as exc:
        MoodleWorksheetRowModel(
            **default_valid_model(),
            grade_type=GradeType.pass_fail,
            grade_numeric=50.0,
            grade_pass_fail=PassFailGrade.failed,
        )

    assert "Pass/fail grade requires grade_pass_fail only" in str(exc.value)


def test_pass_fail_grade_missing_pass_fail_value_fails():
    with pytest.raises(ValidationError) as exc:
        MoodleWorksheetRowModel(
            **default_valid_model(),
            grade_type=GradeType.pass_fail,
        )

    assert "Pass/fail grade requires grade_pass_fail only" in str(exc.value)
