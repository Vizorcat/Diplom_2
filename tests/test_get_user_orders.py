import pytest
import allure
from utils.api import StellarBurgersAPI
from utils.helpers import generate_random_email, generate_random_string


@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.api = StellarBurgersAPI()
        self.valid_email = generate_random_email()
        self.valid_password = generate_random_string(8)
        self.valid_name = generate_random_string(6)

        # Регистрируем пользователя для тестов
        self.api.register_user(
            email=self.valid_email,
            password=self.valid_password,
            name=self.valid_name
        )
        # Логинимся, чтобы получить токен
        self.api.login_user(self.valid_email, self.valid_password)
        yield
        # Удаляем пользователя после тестов
        self.api.delete_user()

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_with_auth_success(self):
        # Сначала создаем заказ
        test_ingredients = ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
        self.api.create_order(ingredients=test_ingredients, auth=True)

        # Получаем заказы
        response = self.api.get_user_orders(auth=True)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert "orders" in response.json(), "В ответе отсутствует список заказов"
        assert len(response.json()["orders"]) > 0, "Список заказов пуст"

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_user_orders_without_auth_fails(self):
        # Создаем новый экземпляр API без токена
        unauth_api = StellarBurgersAPI()
        response = unauth_api.get_user_orders(auth=False)
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "You should be authorised", "Неверное сообщение об ошибке"