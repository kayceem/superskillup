from django.test import RequestFactory, TestCase
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from app.topic import views
from django.urls import reverse
from app.models import Course, Topic


class TestTopicCrud(TestCase):

    def setUp(self):
        self.request = RequestFactory()
        self.admin = User.objects.create_user(username='testadmin', email='test@ramailo.tech', password='password123')
        self.course = Course.objects.create(name="Test Course", created_by=self.admin)
        self.topic = Topic.objects.create(name="Test Topic", course=self.course)
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

    def test_create_topic(self):
        data = {"name": "New Topic", "description": "test", "course": self.course.id}
        request = self.generate_request(reverse('create-topic'), self.post, data)
        response = views.create_topic(request)
        assert response.status_code == 201
        assert response.data['status_code'] == 1
        assert 'id' in response.data['data']
        assert data['name'] == response.data['data']['name']

    def test_update_course(self):
        data = {"name": "Updated Topic", "description": "test", "course": self.course.id}
        request = self.generate_request(reverse('update-topic', kwargs={'id': self.topic.id}), self.put, data)
        response = views.update_topic(request, self.topic.id)
        assert response.status_code == 201
        assert response.data['status_code'] == 1
        assert 'id' in response.data['data']
        assert data['name'] == response.data['data']['name']

    def test_get_topics_by_course(self):
        request = self.generate_request(reverse('get-topics-by-course', kwargs={'course_id': self.course.id}))
        response = views.get_topics_by_course(request, self.course.id)
        assert response.status_code == 200
        assert response.data['status_code'] == 1
        assert 'id' in response.data['data'][0]
        assert 'page' in response.data

    def test_get_topic_by_id(self):
        request = self.generate_request(reverse('get-topic-by-id', kwargs={'id': self.topic.id}))
        response = views.get_topic_by_id(request, self.topic.id)
        assert response.status_code == 200
        assert response.data['status_code'] == 1
        assert 'id' in response.data['data']
