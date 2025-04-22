import random
import string
import time

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_email():
    return f"test_{int(time.time())}@example.com"