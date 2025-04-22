import pytest
import allure
from utils.api import StellarBurgersAPI
from utils.helpers import generate_random_email, generate_random_string


@allure.feature("Создание пользователя")
class TestCreateUser:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.api = StellarBurgersAPI()
        self.valid_email = generate_random_email()
        self.valid_password = generate_random_string(8)
        self.valid_name = generate_random_string(6)
        yield
        # Удаление пользователя после теста, если он был создан
        if hasattr(self, "created_user") and self.created_user:
            self.api.login_user(self.valid_email, self.valid_password)
            self.api.delete_user()

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self):
        response = self.api.register_user(
            email=self.valid_email,
            password=self.valid_password,
            name=self.valid_name
        )
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert "accessToken" in response.json(), "В ответе отсутствует accessToken"
        self.created_user = True

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user_fails(self):
        # Сначала создаем пользователя
        self.api.register_user(
            email=self.valid_email,
            password=self.valid_password,
            name=self.valid_name
        )
        self.created_user = True

        # Пытаемся создать такого же пользователя снова
        response = self.api.register_user(
            email=self.valid_email,
            password=self.valid_password,
            name=self.valid_name
        )
        assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
        assert response.json()["message"] == "User already exists", "Неверное сообщение об ошибке"

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field_fails(self, missing_field):
        user_data = {
            "email": self.valid_email,
            "password": self.valid_password,
            "name": self.valid_name
        }
        del user_data[missing_field]

        response = self.api.register_user(**user_data)
        assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
        assert "error" in response.json(), "В ответе отсутствует поле error"