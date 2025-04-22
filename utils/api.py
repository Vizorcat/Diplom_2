import requests


class StellarBurgersAPI:
    BASE_URL = "https://stellarburgers.nomoreparties.site/api"

    def __init__(self):
        self.session = requests.Session()
        self.token = None

    def register_user(self, email, password, name):
        url = f"{self.BASE_URL}/auth/register"
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        return self.session.post(url, json=payload)

    def login_user(self, email, password):
        url = f"{self.BASE_URL}/auth/login"
        payload = {
            "email": email,
            "password": password
        }
        response = self.session.post(url, json=payload)
        if response.status_code == 200:
            self.token = response.json().get("accessToken")
        return response

    def delete_user(self):
        url = f"{self.BASE_URL}/auth/user"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        return self.session.delete(url, headers=headers)

    def update_user(self, email=None, password=None, name=None):
        url = f"{self.BASE_URL}/auth/user"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        payload = {}
        if email is not None:
            payload["email"] = email
        if password is not None:
            payload["password"] = password
        if name is not None:
            payload["name"] = name
        return self.session.patch(url, headers=headers, json=payload)

    def create_order(self, ingredients, auth=True):
        url = f"{self.BASE_URL}/orders"
        headers = {"Authorization": f"Bearer {self.token}"} if auth and self.token else {}
        payload = {"ingredients": ingredients}
        return self.session.post(url, headers=headers, json=payload)

    def get_user_orders(self, auth=True):
        url = f"{self.BASE_URL}/orders"
        headers = {"Authorization": f"Bearer {self.token}"} if auth and self.token else {}
        return self.session.get(url, headers=headers)