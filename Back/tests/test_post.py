import pytest
from core.config import redis
from tests.conftest import ac
from typing import TYPE_CHECKING
from fastapi import status

if TYPE_CHECKING:
    from httpx import AsyncClient


# pytest  -vv -s  tests/test_post.py::TestAuth - запуск тестов

class TestAuth:

    async def test_register(self, ac: "AsyncClient"):
        user_data = {"email": "test_11_22@test.com", "username": "nametest", "password": "passwordtest", "password_confirm": "passwordtest"}
        response = await ac.post("/register", params=user_data)
        assert response.json() == {'status_code': status.HTTP_200_OK, 'data': 'Для завершения регистрации проверьте свой почтовый ящик'}

    async def test_verify(self, ac: "AsyncClient"):
        token = await redis.keys()
        response = await ac.get(f"/verified/{token[-1]}")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("login", ["test_11_22@test.com", "nametest"])
    async def test_login(self, ac: "AsyncClient", login):
        user_data = {"username": login, "password": "passwordtest"}
        response = await ac.post("/login", data=user_data)
        assert response.json() == {"status_code": status.HTTP_200_OK, "data": "Пользователь вошел в систему"}

    async def test_logout(self, ac: "AsyncClient"):
        response = await ac.post("/logout")
        assert response.status_code == status.HTTP_200_OK


class TestOperation:
    async def test_subscribe(self, ac: "AsyncClient"):
        user_data = {"email": "test_11_22@test.com"}
        response = await ac.post("/subscribe", json=user_data)
        assert response.json() == {"status_code": status.HTTP_200_OK, "data": "Вы подписались на рассылку"}

    async def test_reset_password_code(self, ac: "AsyncClient"):
        user_data = {"email": "test_11_22@test.com"}
        response = await ac.post("/reset-password/code-confirm", json=user_data)
        assert response.json() == {"status_code": status.HTTP_200_OK, "data": "Письмо отправлено на почту"}
