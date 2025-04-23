import pytest
import allure
from utils.api import StellarBurgersAPI



@allure.feature("Изменение данных пользователя")
class TestUpdateUser:
    @allure.title("Изменение email с авторизацией")
    def test_update_email_with_auth_success(self, api_client):
        client, data = api_client
        client.register_user(**data)
        data['created_user'] = True
        client.login_user(data['email'], data['password'])

        new_email = "updated_" + data['email']
        response = client.update_user(email=new_email)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert response.json()["user"]["email"] == new_email, "Email не обновился"

    @allure.title("Изменение пароля с авторизацией")
    def test_update_password_with_auth_success(self, api_client):
        client, data = api_client
        client.register_user(**data)
        data['created_user'] = True
        client.login_user(data['email'], data['password'])

        new_password = "updated_" + data['password']
        response = client.update_user(password=new_password)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        login_response = client.login_user(data['email'], new_password)
        assert login_response.status_code == 200, "Не удалось войти с новым паролем"

    @allure.title("Изменение имени с авторизацией")
    def test_update_name_with_auth_success(self, api_client):
        client, data = api_client
        client.register_user(**data)
        data['created_user'] = True
        client.login_user(data['email'], data['password'])

        new_name = "updated_" + data['name']
        response = client.update_user(name=new_name)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert response.json()["user"]["name"] == new_name, "Имя не обновилось"

    @allure.title("Изменение данных без авторизации")
    def test_update_user_without_auth_fails(self, api_client):
        client, data = api_client
        new_name = "unauth_update_" + data['name']
        unauth_api = StellarBurgersAPI()
        response = unauth_api.update_user(name=new_name)
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "You should be authorised", "Неверное сообщение об ошибке"