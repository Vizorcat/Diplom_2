import pytest
import allure
from utils.api import StellarBurgersAPI


@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_with_auth_success(self, api_client):
        client, data = api_client
        client.register_user(**data)
        data['created_user'] = True
        client.login_user(data['email'], data['password'])

        test_ingredients = ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
        client.create_order(ingredients=test_ingredients, auth=True)

        response = client.get_user_orders(auth=True)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert "orders" in response.json(), "В ответе отсутствует список заказов"
        assert len(response.json()["orders"]) > 0, "Список заказов пуст"

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_user_orders_without_auth_fails(self, api_client):
        client, _ = api_client
        unauth_api = StellarBurgersAPI()
        response = unauth_api.get_user_orders(auth=False)
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "You should be authorised", "Неверное сообщение об ошибке"