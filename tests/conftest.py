import pytest
from fastapi.testclient import TestClient

from fat_free_api.app import app


# Metodologia DRY para evitar repetição de código
@pytest.fixture
def client():
    return TestClient(app)
