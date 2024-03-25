from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from app.app_admin import views
from django.urls import reverse
from app.shared.authentication import AdminAuthentication


class TestAdminLogin(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.admin = User.objects.create_user(username='testadmin', email='test@ramailo.tech', password='password123')
        self.post = 'post'
        self.get = 'get'
        self.put = 'put'

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

    def test_admin_login(self):
        data = {"username": "testadmin", "password": "password123"}
        request = self.generate_request(reverse('admin-login'), self.post, data)
        response = views.login_admin(request)
        assert response.status_code == 200
        assert response.data['status_code'] == 1
        assert 'access_token' in response.data['data']
        access_token = response.data['data']['access_token']
        # Test JWT
        request = self.generate_request(reverse('admin-login'), self.post, data, access_token)
        admin, _ = AdminAuthentication().authenticate(request=request)
        assert admin.username == data['username']
