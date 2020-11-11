import pytest
import pytest_mock
from httpx import AsyncClient

from app import app


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
@pytest_mock.mock.patch('app.users', return_value={"sdf": "asd"})
async def test_users(client):
    response = await client.get("/")
    return response
    # assert response.status_code == 200
    # assert response.json() == {'message':  'hello'}


# создать mocker
# @pytest.mark.asincio
# @pytest_mock.mock.patch('app./cache', return_value={1: 23})  # ???
# @pytest_mock.mock.patch('', return_value=)
# async def test_cache_return(client, mocker):
#     response = await client.get('/cache')
#     print(response.json())
