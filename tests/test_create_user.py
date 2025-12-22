import pytest
import allure
from utils.api import StellarBurgersAPI


@allure.feature("Создание пользователя")
class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, api_client):
        client, data = api_client
        response = client.register_user(**data)
        data['created_user'] = True
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert "accessToken" in response.json(), "В ответе отсутствует accessToken"

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user_fails(self, api_client):
        client, data = api_client
        client.register_user(**data)
        data['created_user'] = True

        response = client.register_user(**data)
        assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
        assert response.json()["message"] == "User already exists", "Неверное сообщение об ошибке"

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field_fails(self, api_client, missing_field):
        client, data = api_client
        user_data = data.copy()
        del user_data[missing_field]

        response = client.register_user(**user_data)
        assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
        assert "error" in response.json(), "В ответе отсутствует поле error"