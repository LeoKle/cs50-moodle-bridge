import os


def pytest_configure():
    os.environ.setdefault("GITHUB_APP_ID", "123")
    os.environ.setdefault("GITHUB_INSTALLATION_ID", "321")
    os.environ.setdefault("GITHUB_PRIVATE_KEY_BASE64", "ZHVtbXk=")  # "dummy"
    os.environ.setdefault("GITHUB_USE_AUTH", "false")
