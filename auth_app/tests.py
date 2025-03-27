import json
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from join.settings import TOKEN_EXPIRATION_TIME
from .models import ExpiringToken

User = get_user_model()

class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="securepassword",
            first_name="Test"
        )
        self.token = ExpiringToken.objects.create(user=self.user, expires_at=timezone.now() + TOKEN_EXPIRATION_TIME)
        self.login_url = "/auth/login/"
        self.logout_url = "/auth/logout/"
        self.auth_url = "/auth/"

    def test_login_success(self):
        response = self.client.post(
            self.login_url,
            data=json.dumps({"email": "test@example.com", "password": "securepassword"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_credentials(self):
        response = self.client.post(
            self.login_url,
            data=json.dumps({"email": "test@example.com", "password": "wrongpassword"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        
        response = self.client.post(
            self.login_url,
            data=json.dumps({"email": "test@example.com", "password": "securepassword"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_logout_without_token(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.auth_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_id"], self.user.id)

    def test_auth_expired_token(self):
        self.token.expires_at = timezone.now() - TOKEN_EXPIRATION_TIME
        self.token.save()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.auth_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    def test_auth_no_token(self):
        response = self.client.get(self.auth_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    def test_auth_valid_token_with_fresh_expiration(self):
        self.token.expires_at = timezone.now() + timezone.timedelta(minutes=10)
        self.token.save()
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.auth_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_id"], self.user.id)

    def test_auth_token_exactly_at_expiration(self):
        self.token.expires_at = timezone.now()
        self.token.save()
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.auth_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Token expired, please log in again")

    def test_logout_with_expired_token(self):
        self.token.expires_at = timezone.now() - timezone.timedelta(days=1)
        self.token.save()
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "No active session or token already expired")

    def test_login_invalid_email_format(self):
        response = self.client.post(
            self.login_url,
            data=json.dumps({"email": "invalidemail", "password": "securepassword"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        
    def test_login_password_too_short(self):
        data = {'email': 'user@example.com', 'password': 'short'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            
    def test_logout_token_deletion(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.auth_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data) 
        self.assertEqual(response.data["detail"], "Invalid token.")

    def test_auth_inactive_user(self):
        self.user.is_active = False
        self.user.save()

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.auth_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "User inactive or deleted.")

    def test_token_for_different_users(self):
        user2 = User.objects.create_user(
            email="test2@example.com",
            password="securepassword2",
            first_name="Test2"
        )
        response = self.client.post(
            self.login_url,
            data=json.dumps({"email": "test2@example.com", "password": "securepassword2"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data["user_id"], self.user.id) 