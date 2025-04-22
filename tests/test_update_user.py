import pytest
import allure
from utils.api import StellarBurgersAPI
from utils.helpers import generate_random_email, generate_random_string


@allure.feature("Изменение данных пользователя")
class TestUpdateUser:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.api = StellarBurgersAPI()
        self.original_email = generate_random_email()
        self.original_password = generate_random_string(8)
        self.original_name = generate_random_string(6)

        # Регистрируем пользователя для тестов
        self.api.register_user(
            email=self.original_email,
            password=self.original_password,
            name=self.original_name
        )
        # Логинимся, чтобы получить токен
        self.api.login_user(self.original_email, self.original_password)
        yield
        # Удаляем пользователя после тестов
        self.api.delete_user()

    @allure.title("Изменение email с авторизацией")
    def test_update_email_with_auth_success(self):
        new_email = "updated_" + self.original_email
        response = self.api.update_user(email=new_email)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert response.json()["user"]["email"] == new_email, "Email не обновился"

    @allure.title("Изменение пароля с авторизацией")
    def test_update_password_with_auth_success(self):
        new_password = "updated_" + self.original_password
        response = self.api.update_user(password=new_password)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        # Проверяем, что с новым паролем можно залогиниться
        login_response = self.api.login_user(self.original_email, new_password)
        assert login_response.status_code == 200, "Не удалось войти с новым паролем"

    @allure.title("Изменение имени с авторизацией")
    def test_update_name_with_auth_success(self):
        new_name = "updated_" + self.original_name
        response = self.api.update_user(name=new_name)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert response.json()["user"]["name"] == new_name, "Имя не обновилось"

    @allure.title("Изменение данных без авторизации")
    def test_update_user_without_auth_fails(self):
        # Создаем новый экземпляр API без токена
        unauth_api = StellarBurgersAPI()
        new_name = "unauth_update_" + self.original_name
        response = unauth_api.update_user(name=new_name)
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "You should be authorised", "Неверное сообщение об ошибке"