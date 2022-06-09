import pytest


@pytest.fixture
def input_value() -> str:
    base_url = "http://localhost:8080/"
    return base_url
