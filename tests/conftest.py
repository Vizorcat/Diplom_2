import pytest
import allure
from utils.helpers import generate_random_email, generate_random_string
from utils.api import StellarBurgersAPI

@pytest.fixture
def api_client():
    client = StellarBurgersAPI()
    test_data = {
        'email': generate_random_email(),
        'password': generate_random_string(8),
        'name': generate_random_string(6),
        'created_user': False
    }

    yield client, test_data

    # Teardown
    if test_data['created_user']:
        try:
            client.login_user(test_data['email'], test_data['password'])
            client.delete_user()
        except Exception as e:
            allure.attach(f"Cleanup error: {str(e)}", name="Teardown Error")