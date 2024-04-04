from django.test import RequestFactory, TestCase
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from app.course import views
from django.urls import reverse
from app.models import UserProfile
from app.models import Course
import pytest


class TestCourseCrud(TestCase):
    @pytest.mark.django_db(databases=['test'])
    def setUp(self):
        self.request = RequestFactory()
        self.admin = User.objects.create_user(username='testadmin', email='test@ramailo.tech', password='password123')
        self.user = UserProfile.objects.create(name='testuser', email='testuser@ramailo.tech', password='password123')
        self.course = Course.objects.create(name="Test Course", created_by=self.admin)
        self.post = 'post'
        self.get = 'get'
        self.put = 'put'

    def generate_request(self, url, method='get', data=None):
        content_type = 'application/json'
        if method == self.post:
            request = self.request.post(url, data, content_type)
        if method == self.get:
            request = self.request.get(url)
        if method == self.put:
            request = self.request.put(url, data, content_type)
        force_authenticate(request, user=self.admin)
        return request

    def test_create_course(self):
        data = {"name": "New Course", "description": "test"}
        request = self.generate_request(reverse('create-course'), self.post, data)
        response = views.create_course(request)
        assert response.status_code == 201
        assert response.data['status_code'] == 1
        assert 'id' in response.data['data']
        assert data['name'] == response.data['data']['name']

    def test_get_all_courses(self):
        request = self.generate_request(reverse('get-all-courses'))
        response = views.get_all_courses(request)

        assert response.status_code == 200
        assert response.data['status_code'] == 1
        assert 'id' in response.data['data'][0]
        assert 'page' in response.data

    def test_get_course_by_id(self):
        request = self.generate_request(reverse('get-course-by-id', kwargs={'id': self.course.id}))
        response = views.get_course_by_id(request, self.course.id)
        assert response.status_code == 200
        assert response.data['status_code'] == 1
        assert 'id' in response.data['data']

    def test_update_course(self):
        data = {"name": "Updated Course", "description": "test"}
        request = self.generate_request(reverse('update-course', kwargs={'id': self.course.id}), self.put, data)
        response = views.update_course(request, self.course.id)
        assert response.status_code == 201
        assert response.data['status_code'] == 1
        assert 'id' in response.data['data']
        assert data['name'] == response.data['data']['name']
