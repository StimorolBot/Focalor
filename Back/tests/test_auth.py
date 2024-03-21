from httpx import AsyncClient
from tests.conftest import ac


# pytest  -vv -s  tests/test_auth.py::TestAuth - запуск тестов

class TestAuth:

    async def test_register(self, ac: AsyncClient):
        user_date = {"email": "email@my.com", "username": "myNameTest", "password": "passwordtest", "password_confirm": "passwordtest"}
        response = await ac.post("/register", params=user_date)
        assert response.json() == {'status_code': 200, 'data': 'Для завершения регистрации проверьте свой почтовый ящик'}


