import pytest
from fastapi import status
from tests.conftest import ac
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import AsyncClient


# pytest  -vv -s  tests/test_page.py::TestPage запуск тестов


class TestPage:
    @pytest.mark.parametrize("url", ["/test_page", "/register?password=test", "123", "/'"])
    async def test_page_not_found(self, ac: "AsyncClient", url: str):
        response = await ac.get(url=url)
        assert response.status_code == status.HTTP_200_OK
