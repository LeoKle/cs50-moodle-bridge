import sys
from pathlib import Path

import pytest

# Add src directory to Python path
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


@pytest.fixture(autouse=True)
def reset_streamlit_session():
    """Reset streamlit session state before each test."""
    yield
