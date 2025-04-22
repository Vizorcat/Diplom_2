import pytest
import allure
from utils.api import StellarBurgersAPI
from utils.helpers import generate_random_email, generate_random_string


@allure.feature("Создание заказа")
class TestCreateOrder:
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
        yield
        # Удаляем пользователя после тестов
        self.api.login_user(self.valid_email, self.valid_password)
        self.api.delete_user()

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients_success(self):
        # Предполагаем, что есть какие-то тестовые ингредиенты
        # В реальном тесте нужно получить реальные ID ингредиентов из API
        test_ingredients = ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]

        response = self.api.create_order(ingredients=test_ingredients, auth=True)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert "order" in response.json(), "В ответе отсутствует информация о заказе"
        assert "number" in response.json()["order"], "В ответе отсутствует номер заказа"

    @allure.title("Создание заказа без авторизации с ингредиентами")
    def test_create_order_without_auth_with_ingredients_success(self):
        test_ingredients = ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]

        response = self.api.create_order(ingredients=test_ingredients, auth=False)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert "order" in response.json(), "В ответе отсутствует информация о заказе"

    @allure.title("Создание заказа без ингредиентов")
    @pytest.mark.parametrize("auth", [True, False], ids=["with_auth", "without_auth"])
    def test_create_order_without_ingredients_fails(self, auth):
        response = self.api.create_order(ingredients=[], auth=auth)
        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
        assert response.json()["message"] == "Ingredient ids must be provided", "Неверное сообщение об ошибке"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @pytest.mark.parametrize("auth", [True, False], ids=["with_auth", "without_auth"])
    def test_create_order_with_invalid_ingredient_hash_fails(self, auth):
        invalid_ingredients = ["invalid_hash_1", "invalid_hash_2"]

        response = self.api.create_order(ingredients=invalid_ingredients, auth=auth)
        assert response.status_code == 500, f"Ожидался код 500, получен {response.status_code}"