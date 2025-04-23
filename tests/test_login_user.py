import pytest
import allure
from utils.api import StellarBurgersAPI



@allure.feature("Авторизация пользователя")
class TestLoginUser:
    @allure.title("Успешная авторизация существующего пользователя")
    def test_login_existing_user_success(self, api_client):
        client, data = api_client
        client.register_user(**data)
        data['created_user'] = True

        response = client.login_user(data['email'], data['password'])
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert "accessToken" in response.json(), "В ответе отсутствует accessToken"

    @allure.title("Авторизация с неверным email")
    def test_login_with_wrong_email_fails(self, api_client):
        client, data = api_client
        response = client.login_user("wrong_" + data['email'], data['password'])
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"

    @allure.title("Авторизация с неверным паролем")
    def test_login_with_wrong_password_fails(self, api_client):
        client, data = api_client
        response = client.login_user(data['email'], "wrong_" + data['password'])
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"