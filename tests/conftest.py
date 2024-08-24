import pytest
from fastapi.testclient import TestClient  # noqa: F401

from fast_rafa.app import app  # noqa: F401


@pytest.fixture
def client():
    return TestClient(app)
