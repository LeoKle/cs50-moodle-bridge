import pytest


@pytest.fixture(autouse=True)
def reset_streamlit_session():
    """Reset streamlit session state before each test."""
    yield
