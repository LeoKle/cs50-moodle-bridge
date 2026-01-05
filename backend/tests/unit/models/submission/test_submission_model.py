from datetime import datetime

from dateutil import tz

from models.submission import SubmissionModel


def test_timestamp_utc():
    sample = {
        "archive": "https://github.com/me50/github_name/archive/hash_value.zip",
        "checks_passed": 5,
        "checks_run": 5,
        "github_id": 987654321,
        "github_url": "https://github.com/me50/github_name/tree/hash_value",
        "github_username": "octocat",
        "name": "Test Submission UTC",
        "slug": "hsddigitallabor/problems/adg2025/utc",
        "style50_score": 1.0,
        "timestamp": "2025-12-01T18:30:00Z",  # UTC time
    }

    submission = SubmissionModel(**sample)
    dt = submission.timestamp

    expected_dt = datetime(2025, 12, 1, 18, 30, 0, tzinfo=tz.UTC)

    assert dt.replace(tzinfo=None) == expected_dt.replace(tzinfo=None)
    assert dt.utcoffset() == expected_dt.utcoffset()


def test_timestamp_iso_with_offset():
    sample = {
        "archive": "https://github.com/me50/github_name/archive/hash_value.zip",
        "checks_passed": 10,
        "checks_run": 10,
        "github_id": 444555666,
        "github_url": "https://github.com/me50/github_name/tree/hash_value",
        "github_username": "octocat",
        "name": "Test Submission ISO Offset",
        "slug": "hsddigitallabor/problems/adg2025/iso-offset",
        "style50_score": 1.0,
        "timestamp": "2025-12-01T20:20:07+01:00",  # CET offset
    }

    submission = SubmissionModel(**sample)
    dt = submission.timestamp

    cet_tz = tz.gettz("Europe/Berlin")
    expected_dt = datetime(2025, 12, 1, 20, 20, 7, tzinfo=cet_tz)

    assert dt.replace(tzinfo=None) == expected_dt.replace(tzinfo=None)
    assert dt.utcoffset() == expected_dt.utcoffset()


def test_timestamp_date_time_and_timezone():
    sample = {
        "archive": "https://github.com/me50/github_name/archive/hash_value.zip",
        "checks_passed": 13,
        "checks_run": 13,
        "github_id": 123456789,
        "github_url": "https://github.com/me50/github_name/tree/hash_value",
        "github_username": "octocat",
        "name": None,
        "slug": "hsddigitallabor/problems/adg2025/intervals",
        "style50_score": 1.0,
        "timestamp": "Mon, 01 Dec 2025 08:20:07PM CET",
    }

    submission = SubmissionModel(**sample)
    dt = submission.timestamp

    berlin_tz = tz.gettz("Europe/Berlin")
    expected_dt = datetime(2025, 12, 1, 20, 20, 7, tzinfo=berlin_tz)

    assert dt.replace(tzinfo=None) == expected_dt.replace(tzinfo=None)
    assert dt.utcoffset() == expected_dt.utcoffset()


def test_timestamp_with_am_pm_midnight():
    sample = {
        "archive": "https://github.com/me50/github_name/archive/hash_value.zip",
        "checks_passed": 2,
        "checks_run": 2,
        "github_id": 777888999,
        "github_url": "https://github.com/me50/github_name/tree/hash_value",
        "github_username": "octocat",
        "name": "Test Submission Midnight",
        "slug": "hsddigitallabor/problems/adg2025/midnight",
        "style50_score": 1.0,
        "timestamp": "Thu, 04 Dec 2025 12:00:00AM CET",
    }

    submission = SubmissionModel(**sample)
    dt = submission.timestamp

    cet_tz = tz.gettz("Europe/Berlin")
    expected_dt = datetime(2025, 12, 4, 0, 0, 0, tzinfo=cet_tz)

    assert dt.replace(tzinfo=None) == expected_dt.replace(tzinfo=None)
    assert dt.utcoffset() == expected_dt.utcoffset()
