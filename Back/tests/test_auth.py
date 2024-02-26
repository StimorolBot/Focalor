from fastapi import status
from httpx import AsyncClient
from tests.conftest import ac


# pytest -v -s tests/ - запуск тестов

class TestAuth:

    async def test_register(self, ac: AsyncClient):
        user_date = {"email": "maxim@test.reg", "username": "maxim_test", "password": "passwordtest"}
        response = await ac.post("/register", data=user_date)

        assert response.json() == {
            "status_code": status.HTTP_200_OK,
            "detail": "Для завершения регистрации проверьте свой почтовый ящик"
        }
