import pytest
import allure
from utils.api import StellarBurgersAPI
from utils.helpers import generate_random_email, generate_random_string


@allure.feature("Авторизация пользователя")
class TestLoginUser:
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

    @allure.title("Успешная авторизация существующего пользователя")
    def test_login_existing_user_success(self):
        response = self.api.login_user(
            email=self.valid_email,
            password=self.valid_password
        )
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert "accessToken" in response.json(), "В ответе отсутствует accessToken"

    @allure.title("Авторизация с неверным email")
    def test_login_with_wrong_email_fails(self):
        response = self.api.login_user(
            email="wrong_" + self.valid_email,
            password=self.valid_password
        )
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"

    @allure.title("Авторизация с неверным паролем")
    def test_login_with_wrong_password_fails(self):
        response = self.api.login_user(
            email=self.valid_email,
            password="wrong_" + self.valid_password
        )
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"