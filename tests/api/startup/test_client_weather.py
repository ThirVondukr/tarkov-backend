import datetime

import httpx
import pytest
from starlette import status

endpoint_url = "/client/weather"


@pytest.fixture
async def response(http_client: httpx.AsyncClient, freeze_time) -> httpx.Response:
    return await http_client.post(endpoint_url)


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_should_return_correct_time_in_weather(response: httpx.Response):
    weather = response.json()["data"]

    now = datetime.datetime.now()
    delta = datetime.timedelta(
        hours=now.hour,
        minutes=now.minute,
        seconds=now.second,
        microseconds=now.microsecond,
    )
    accelerated_time = now + delta * weather["acceleration"]
    accelerated_time.replace(
        year=now.year,
        month=now.month,
        day=now.day,
    )
    date_str = accelerated_time.strftime("%Y-%m-%d")
    time_str = accelerated_time.strftime("%H:%M:%S")

    assert weather["weather"]["timestamp"] == int(freeze_time)

    assert weather["weather"]["date"] == date_str
    assert weather["date"] == date_str

    assert weather["weather"]["time"] == accelerated_time.strftime("%Y-%m-%d %H:%M:%S")
    assert weather["time"] == time_str
