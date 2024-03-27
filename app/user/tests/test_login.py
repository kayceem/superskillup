import json
from django.test import RequestFactory, TestCase
from app.user import views
from django.urls import reverse
from app.shared.authentication import UserAuthentication
from app.models import UserProfile


class TestUserLogin(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.user = UserProfile.objects.create(name='testuser', email='testuser@ramailo.tech', password='password123', is_verified=True)
        self.post = 'post'
        self.get = 'get'
        self.put = 'put'
        self.new_user: str

    def generate_request(self, url, method='get', data=None, token=None):
        content_type = 'application/json'
        headers = {'Authorization': f'Bearer {token}'} if token else None
        if method == self.post:
            request = self.request.post(path=url, data=data, content_type=content_type, headers=headers)
        if method == self.get:
            request = self.request.get(url)
        if method == self.put:
            request = self.request.put(url, data, content_type)
        return request

    def test_create_user(self):
        data = {"name": "user", "email": "new@ramailo.tech", "password": "password123"}
        request = self.generate_request(reverse('register-user'), self.post, data)
        response = views.register_user(request)
        assert response.status_code == 201
        assert response.data['status_code'] == 1
        assert 'Message' in response.data['data']
        self.new_user = UserProfile.objects.filter(email=data['email']).first()
        # verify otp
        verify_data = {"email": f"{self.new_user.email}", "otp": f"{self.new_user.otp}"}
        verify_request = self.generate_request(reverse('check-otp'), self.post, verify_data)
        response = views.check_otp(verify_request)
        assert response.status_code == 201
        assert response.data['status_code'] == 1
        assert 'user' in response.data['data']

    def test_user_login(self):
        data = {"email": "testuser@ramailo.tech", "password": "password123"}
        request = self.generate_request(reverse('login-user'), self.post, data)
        response = views.login_user(request)
        assert response.status_code == 200
        assert response.data['status_code'] == 1
        assert 'access_token' in response.data['data']
        access_token = response.data['data']['access_token']
        # Test JWT
        request = self.generate_request(reverse('login-user'), self.post, data, access_token)
        user, _ = UserAuthentication().authenticate(request=request)
        assert user.email == data['email']
