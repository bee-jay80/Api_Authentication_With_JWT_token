# from django.test import TestCase

# # Create your tests here.

from django.test import TestCase
from rest_framework.test import APIClient
from..models import User, Organisation

class RegisterTest(TestCase):
    def test_register_user_successfully(self):
        client = APIClient()
        response = client.post('/auth/register/', {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'password123',
            'phone': '1234567890'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], 'uccess')
        self.assertEqual(response.data['message'], 'Registration successful')

    def test_register_user_with_missing_fields(self):
        client = APIClient()
        response = client.post('/auth/register/', {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@example.com'
        })
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data['status'], 'Bad request')
        self.assertEqual(response.data['message'], 'Registration unsuccessful')

    def test_register_user_with_duplicate_email(self):
        client = APIClient()
        User.objects.create_user('johndoe@example.com', 'password123')
        response = client.post('/auth/register/', {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'password123',
            'phone': '1234567890'
        })
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data['status'], 'Bad request')
        self.assertEqual(response.data['message'], 'Registration unsuccessful')

class LoginTest(TestCase):
    def test_login_user_successfully(self):
        client = APIClient()
        user = User.objects.create_user('johndoe@example.com', 'password123')
        response = client.post('/auth/login/', {
            'email': 'johndoe@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'uccess')
        self.assertEqual(response.data['message'], 'Login successful')

    def test_login_user_with_invalid_credentials(self):
        client = APIClient()
        response = client.post('/auth/login/', {
            'email': 'johndoe@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['status'], 'Bad request')