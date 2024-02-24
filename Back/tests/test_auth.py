from conftest import client
from fastapi import status


# pytest -v tests/ - запуск тестов

def test_register():
    response = client.post("/register", json={
        "email": "test@test.com",
        "username": "username",
        "password": "password"
    })
    assert response.status_code == status.HTTP_200_OK, "[!] Не удалось зарегистрировать пользователя"


def test_login_email():
    response = client.post("/login", json={
        "username": "test@test.com",
        "password": "password"
    })

    print(response)


def test_login_username():
    response = client.post("/login", json={
        "username": "username",
        "password": "password"
    })


def test_reset_password():
    ...


def test_subscribe_newsletter():
    ...


def test_logout():
    ...
