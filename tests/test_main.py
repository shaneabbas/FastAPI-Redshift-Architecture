import pytest
from httpx import AsyncClient
from core.models.database import database
import main
from main import app
from parameters import LOG_IN_PAYLOAD, BASE_URL, TEST_RESPONSE_CREATE_CLIENT_PAYLOAD, \
    TEST_REQUEST_CREATE_CLIENT_PAYLOAD, TEST_RESPONSE_CREATE_CAMPAIGN_PAYLOAD, \
    TEST_REQUEST_CREATE_CAMPAIGN_PAYLOAD, TEST_LOGIN_URL, TEST_REQUEST_CREATE_KEYWORD_PAYLOAD, \
    TEST_RESPONSE_CREATE_KEYWORD_PAYLOAD


# TO RUN ALL TESTS USING PYTEST
# pytest
# TO RUN SPECIFIC TEST USING PYTEST
# pytest -v tests/test_main.py::test_campaigns_get


# ### CAMPAIGNS ###
# GET
@pytest.mark.asyncio
async def test_campaigns_get():
    await main.startup()
    try:
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            token = await ac.post(TEST_LOGIN_URL, data=LOG_IN_PAYLOAD)
            token = token.json()
            token_ = token['access_token']
            headers_ = {'Authorization': 'Bearer {}'.format(token_)}
            response = await ac.get("/campaigns/113/", headers=headers_)
        assert response.status_code == 200
        # assert response.json() == TEST_RESPONSE_GET_CAMPAIGN_PAYLOAD
    finally:
        await main.shutdown()


@pytest.mark.asyncio
async def test_campaigns_get_list_locafy():
    await main.startup()
    try:
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            token = await ac.post(TEST_LOGIN_URL, data=LOG_IN_PAYLOAD)
            token = token.json()
            token_ = token['access_token']
            headers_ = {'Authorization': 'Bearer {}'.format(token_)}
            response = await ac.get("/campaigns/list/locafy/?page=1&size=50", headers=headers_)
        assert response.status_code == 200
        # assert response.json() == TEST_RESPONSE_GET_CAMPAIGN_PAYLOAD
    finally:
        await main.shutdown()


@pytest.mark.asyncio
async def test_campaigns_get_list_locafy_client_id():
    await main.startup()
    try:
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            token = await ac.post(TEST_LOGIN_URL, data=LOG_IN_PAYLOAD)
            token = token.json()
            token_ = token['access_token']
            headers_ = {'Authorization': 'Bearer {}'.format(token_)}
            response = await ac.get("/campaigns/list/locafy/123/", headers=headers_)
        assert response.status_code == 200
        # assert response.json() == TEST_RESPONSE_GET_CAMPAIGN_PAYLOAD
    finally:
        await main.shutdown()


# CREATE
@pytest.mark.asyncio
async def test_campaigns_create():
    await main.startup()
    payload = TEST_REQUEST_CREATE_CAMPAIGN_PAYLOAD
    try:
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            token = await ac.post(TEST_LOGIN_URL, data=LOG_IN_PAYLOAD)
            token = token.json()
            token_ = token['access_token']
            headers_ = {'Authorization': 'Bearer {}'.format(token_)}
            response = await ac.post("/campaigns/create/", headers=headers_, json=payload)

            if response.status_code == 201:
                data = response.json()
                id_ = data["campaign_id"]
                await ac.delete("/campaigns/delete/{}/".format(id_), headers=headers_)
        assert response.status_code == 201
        TEST_RESPONSE_CREATE_CAMPAIGN_PAYLOAD['campaign_id'] = id_
        TEST_RESPONSE_CREATE_CAMPAIGN_PAYLOAD['business_name'] = data['business_name']
        # assert response.json() == TEST_RESPONSE_CREATE_CAMPAIGN_PAYLOAD
    finally:
        await main.shutdown()

# ### CAMPAIGNS ###


# ### CLIENTS ###
# GET
@pytest.mark.asyncio
async def test_client_get():
    await main.startup()
    try:
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            token = await ac.post(TEST_LOGIN_URL, data=LOG_IN_PAYLOAD)
            token = token.json()
            token_ = token['access_token']
            headers_ = {'Authorization': 'Bearer {}'.format(token_)}
            response = await ac.get("/clients/34/", headers=headers_)
        assert response.status_code == 200
        # assert response.json() == TEST_RESPONSE_GET_PROXY_PAYLOAD
    finally:
        await main.shutdown()


@pytest.mark.asyncio
async def test_client_get_list():
    await main.startup()
    try:
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            token = await ac.post(TEST_LOGIN_URL, data=LOG_IN_PAYLOAD)
            token = token.json()
            token_ = token['access_token']
            headers_ = {'Authorization': 'Bearer {}'.format(token_)}
            response = await ac.get("/clients/clients/list/?page=1&size=50", headers=headers_)
        assert response.status_code == 200
        # assert response.json() == TEST_RESPONSE_GET_PROXY_PAYLOAD
    finally:
        await main.shutdown()


# CREATE
@pytest.mark.asyncio
async def test_client_create():
    await main.startup()
    req_payload = TEST_REQUEST_CREATE_CLIENT_PAYLOAD
    try:
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            token = await ac.post(TEST_LOGIN_URL, data=LOG_IN_PAYLOAD)
            token = token.json()
            token_ = token['access_token']
            headers_ = {'Authorization': 'Bearer {}'.format(token_)}
            response = await ac.post("/clients/create/", headers=headers_, json=req_payload)

            if response.status_code == 201:
                id_ = response.json()
                client_name = id_["client_name"]
                await ac.delete("/clients/delete/{}/".format(client_name), headers=headers_)
        assert response.status_code == 201
        # TEST_RESPONSE_CREATE_CLIENT_PAYLOAD['id'] = id_
        assert response.json() == TEST_RESPONSE_CREATE_CLIENT_PAYLOAD
    finally:
        await main.shutdown()

# ### CLIENTS ###


# ### GEO GIFS URLS ###
# GET
@pytest.mark.asyncio
async def test_geo_gifs_urls_get_list():
    await main.startup()
    try:
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            token = await ac.post(TEST_LOGIN_URL, data=LOG_IN_PAYLOAD)
            token = token.json()
            token_ = token['access_token']
            headers_ = {'Authorization': 'Bearer {}'.format(token_)}
            response = await ac.get("/geo/gifs/urls/list/?page=1&size=50", headers=headers_)
        assert response.status_code == 200
        # assert response.json() == TEST_RESPONSE_GET_QUERY_PAYLOAD
    finally:
        await main.shutdown()


@pytest.mark.asyncio
async def test_geo_gifs_urls_get_list_campaign_id():
    await main.startup()
    try:
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            token = await ac.post(TEST_LOGIN_URL, data=LOG_IN_PAYLOAD)
            token = token.json()
            token_ = token['access_token']
            headers_ = {'Authorization': 'Bearer {}'.format(token_)}
            response = await ac.get("/geo/gifs/urls/campaign/131/?page=1&size=50", headers=headers_)
        assert response.status_code == 200
        # assert response.json() == {}
    finally:
        await main.shutdown()


@pytest.mark.asyncio
async def test_geo_gifs_urls_get_list_locafy_client_id():
    await main.startup()
    try:
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            token = await ac.post(TEST_LOGIN_URL, data=LOG_IN_PAYLOAD)
            token = token.json()
            token_ = token['access_token']
            headers_ = {'Authorization': 'Bearer {}'.format(token_)}
            response = await ac.get("/geo/gifs/urls/locafy/9bc885bb-e0ce-b48b-d9cb-611c94ea5219/?page=1&size=50",
                                    headers=headers_)
        assert response.status_code == 200
        # assert response.json() == {}
    finally:
        await main.shutdown()


# ### GEO GIFS URLS ###

# ### GEO GRID URLS ###
# GET
@pytest.mark.asyncio
async def test_geo_grid_urls_get_list():
    await main.startup()
    try:
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            token = await ac.post(TEST_LOGIN_URL, data=LOG_IN_PAYLOAD)
            token = token.json()
            token_ = token['access_token']
            headers_ = {'Authorization': 'Bearer {}'.format(token_)}
            response = await ac.get("/geo/grid/urls/list/all/?page=1&size=50", headers=headers_)
        assert response.status_code == 200
        # assert response.json() == TEST_RESPONSE_GET_QUERY_PAYLOAD
    finally:
        await main.shutdown()


@pytest.mark.asyncio
async def test_geo_grid_urls_get_list_campaign_id():
    await main.startup()
    try:
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            token = await ac.post(TEST_LOGIN_URL, data=LOG_IN_PAYLOAD)
            token = token.json()
            token_ = token['access_token']
            headers_ = {'Authorization': 'Bearer {}'.format(token_)}
            response = await ac.get("/geo/grid/urls/113/?page=1&size=50", headers=headers_)
        assert response.status_code == 200
        # assert response.json() == {}
    finally:
        await main.shutdown()


@pytest.mark.asyncio
async def test_geo_grid_urls_get_list_locafy_client_id():
    await main.startup()
    try:
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            token = await ac.post(TEST_LOGIN_URL, data=LOG_IN_PAYLOAD)
            token = token.json()
            token_ = token['access_token']
            headers_ = {'Authorization': 'Bearer {}'.format(token_)}
            response = await ac.get("/geo/grid/urls/locafy/9bc885bb-e0ce-b48b-d9cb-611c94ea5219/?page=1&size=50",
                                    headers=headers_)
        assert response.status_code == 200
        # assert response.json() == {}
    finally:
        await main.shutdown()


# ### GEO GRID URLS ###


# ### KEYWORD ###
# CREATE
@pytest.mark.asyncio
async def test_keyword_create():
    await main.startup()
    payload = TEST_REQUEST_CREATE_KEYWORD_PAYLOAD
    try:
        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            token = await ac.post(TEST_LOGIN_URL, data=LOG_IN_PAYLOAD)
            token = token.json()
            token_ = token['access_token']
            headers_ = {'Authorization': 'Bearer {}'.format(token_)}
            response = await ac.post("/keyword/create/", headers=headers_, json=payload)

            if response.status_code == 201:
                await ac.delete("/keyword/delete/Realty/113/", headers=headers_)
        assert response.status_code == 201
        assert response.json() == TEST_RESPONSE_CREATE_KEYWORD_PAYLOAD
    finally:
        await main.shutdown()

# ### KEYWORD ###
