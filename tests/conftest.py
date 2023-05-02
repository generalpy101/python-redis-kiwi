import json

from pytest import fixture
from redis import Redis

from rest_kv.main import create_app

APP_HOST = "localhost"
APP_PORT = 8000

REDIS_HOST = "localhost"
REDIS_PORT = 6379


def get_redis_client(host, port, db):
    client = Redis(host=host, port=port, decode_responses=True, db=db)
    return client


@fixture(scope="session")
def app_client():
    redis_client = get_redis_client(REDIS_HOST, REDIS_PORT, 1)
    app = create_app(redis_client)
    yield app.test_client()
    redis_client.flushdb()


@fixture(scope="session")
def app_url():
    return f"http://{APP_HOST}:{APP_PORT}"


@fixture(scope="session")
def test_data_1():
    return {
        "test1": "value1",
        "test2": "10",
        "test3": {"inner_key1": "inner_value1", "inner_key2": "3"},
    }


@fixture(scope="session")
def test_data_2():
    return {
        "test1": "value1",
        "test3": {"inner_key1": "inner_value1", "inner_key2": "3"},
    }


@fixture(scope="session")
def test_data_3():
    return {
        "test1": "value_new",
        "test3": {"inner_key1": "inner_value1", "inner_key2": "3"},
    }
