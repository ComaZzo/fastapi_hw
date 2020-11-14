import pytest
import pytest_mock
from httpx import AsyncClient

from main import app


# @pytest.fixture
# async def client():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         yield ac


# @pytest.mark.asyncio
# @pytest_mock.mock.patch('app.users', return_value=False)
# async def test_users(mocker):
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/")
#     assert response.status_code == 200
#     assert response.json() is False


@pytest.mark.asyncio
@pytest_mock.mock.patch('main.users_query_exe', return_value=[])
async def test_users(mocker):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/users")
    assert response.status_code == 200
    assert response.json() == {'data': {}}


@pytest.mark.asyncio
@pytest_mock.mock.patch('main.actions_query_exe', return_value=[])
async def test_actions(mocker):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/actions")
    assert response.status_code == 200
    assert response.json() == {'data': {}}


@pytest.mark.asyncio
@pytest_mock.mock.patch('main.usage_query_exe', return_value=[])
async def test_usage(mocker):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/usage")
    assert response.status_code == 200
    assert response.json() == {'data': {}}


# создать mocker
# @pytest.mark.asincio
# @pytest_mock.mock.patch('app./cache', return_value={1: 23})  # ???
# @pytest_mock.mock.patch('', return_value=)
# async def test_cache_return(client, mocker):
#     response = await client.get('/cache')
#     print(response.json())
