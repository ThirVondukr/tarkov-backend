import datetime
import time

import httpx
import pytest
from starlette import status

endpoint_url = "/client/weather"


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post(endpoint_url)


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_should_return_correct_time_in_weather(response: httpx.Response):
    weather = response.json()["data"]

    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")

    assert weather["weather"]["timestamp"] == int(time.time())

    assert weather["weather"]["date"] == date_str
    assert weather["date"] == date_str

    delta = datetime.timedelta(
        hours=now.hour,
        minutes=now.minute,
        seconds=now.second,
        microseconds=now.microsecond,
    )
    now_accelerated = now + delta * weather["acceleration"]
    time_str = now_accelerated.strftime("%H:%M:%S")

    assert weather["weather"]["time"] == time_str
    assert weather["time"] == time_str
