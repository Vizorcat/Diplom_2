import pytest
import allure
from utils.api import StellarBurgersAPI



@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients_success(self, api_client):
        client, data = api_client
        client.register_user(**data)
        data['created_user'] = True
        client.login_user(data['email'], data['password'])

        test_ingredients = ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
        response = client.create_order(ingredients=test_ingredients, auth=True)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert "order" in response.json(), "В ответе отсутствует информация о заказе"
        assert "number" in response.json()["order"], "В ответе отсутствует номер заказа"

    @allure.title("Создание заказа без авторизации с ингредиентами")
    def test_create_order_without_auth_with_ingredients_success(self, api_client):
        client, data = api_client
        test_ingredients = ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
        response = client.create_order(ingredients=test_ingredients, auth=False)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert "order" in response.json(), "В ответе отсутствует информация о заказе"

    @allure.title("Создание заказа без ингредиентов")
    @pytest.mark.parametrize("auth", [True, False], ids=["with_auth", "without_auth"])
    def test_create_order_without_ingredients_fails(self, api_client, auth):
        client, data = api_client
        if auth:
            client.register_user(**data)
            data['created_user'] = True
            client.login_user(data['email'], data['password'])

        response = client.create_order(ingredients=[], auth=auth)
        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
        assert response.json()["message"] == "Ingredient ids must be provided", "Неверное сообщение об ошибке"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @pytest.mark.parametrize("auth", [True, False], ids=["with_auth", "without_auth"])
    def test_create_order_with_invalid_ingredient_hash_fails(self, api_client, auth):
        client, data = api_client
        if auth:
            client.register_user(**data)
            data['created_user'] = True
            client.login_user(data['email'], data['password'])

        invalid_ingredients = ["invalid_hash_1", "invalid_hash_2"]
        response = client.create_order(ingredients=invalid_ingredients, auth=auth)
        assert response.status_code == 500, f"Ожидался код 500, получен {response.status_code}"