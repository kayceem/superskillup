from django.test import RequestFactory, TestCase
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from app.sub_topic import views
from django.urls import reverse
from app.models import Course, Topic, SubTopic


class TestTopicCrud(TestCase):

    def setUp(self):
        self.request = RequestFactory()
        self.admin = User.objects.create_user(username='testadmin', email='test@ramailo.tech', password='password123')
        self.course = Course.objects.create(name="Test Course")
        self.topic = Topic.objects.create(name="Test Topic", course=self.course)
        self.sub_topic = SubTopic.objects.create(name="Test SubTopic", topic=self.topic)
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

    def test_create_sub_topic(self):
        data = {"name": "New SubTopic", "description": "test", "topic": self.topic.id}
        request = self.generate_request(reverse('create-sub-topic'), self.post, data)
        response = views.create_sub_topic(request)
        assert response.status_code == 201
        assert response.data['status_code'] == 1
        assert 'id' in response.data['data']
        assert data['name'] == response.data['data']['name']

    def test_update_sub_topic(self):
        data = {"name": "Updated SubTopic", "description": "test", "topic": self.topic.id}
        request = self.generate_request(reverse('update-sub-topic', kwargs={'id': self.sub_topic.id}), self.put, data)
        response = views.update_sub_topic(request, self.sub_topic.id)
        assert response.status_code == 201
        assert response.data['status_code'] == 1
        assert 'id' in response.data['data']
        assert data['name'] == response.data['data']['name']

    def test_get_sub_topics_by_topic(self):
        request = self.generate_request(reverse('get-sub-topics-by-topic', kwargs={'id': self.topic.id}))
        response = views.get_sub_topics_by_topic(request, self.topic.id)
        assert response.status_code == 200
        assert response.data['status_code'] == 1
        assert 'id' in response.data['data'][0]
        assert 'page' in response.data

    def test_get_sub_topic_by_id(self):
        request = self.generate_request(reverse('get-sub-topic-by-id', kwargs={'id': self.sub_topic.id}))
        response = views.get_sub_topic_by_id(request, self.sub_topic.id)
        assert response.status_code == 200
        assert response.data['status_code'] == 1
        assert 'id' in response.data['data']
