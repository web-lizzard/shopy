import pytest
from fastapi.testclient import TestClient

from core.app import create_app
from server.products.dependencies import get_sessionmaker


@pytest.fixture(autouse=True)
def app():
    yield create_app()


@pytest.fixture
def client(app):
    yield TestClient(app)


@pytest.fixture(scope="function", autouse=True)
async def session_maker_override(app, session_factory):
    def get_override_session():
        yield session_factory

    app.dependency_overrides[get_sessionmaker] = get_override_session
