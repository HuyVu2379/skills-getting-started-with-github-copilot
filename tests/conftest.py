import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

_BASELINE_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset in-memory activities before and after each test."""
    activities.clear()
    activities.update(copy.deepcopy(_BASELINE_ACTIVITIES))
    yield
    activities.clear()
    activities.update(copy.deepcopy(_BASELINE_ACTIVITIES))


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
