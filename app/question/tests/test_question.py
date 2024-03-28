from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework.test import force_authenticate
from app.models import Course, Question
from django.contrib.auth.models import User
from app.question import views


class TestQuestion(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.user = User.objects.create(username='testuser', email='testuser@ramailo.tech', password='password123')
        self.course = Course.objects.create(name="django")
        self.question = Question.objects.create(question="trying", course=self.course)
        self.post = 'post'
        self.get = 'get'
        self.put = 'put'

    def generate_request(self, url, method='get', data=None, token=None):
        content_type = 'application/json'
        if method == self.post:
            request = self.request.post(path=url, data=data, content_type=content_type)
        if method == self.get:
            request = self.request.get(url)
        if method == self.put:
            request = self.request.put(url, data, content_type)
        force_authenticate(request, user=self.user)
        return request

    def test_create_question(self):
        data = {"question": "What is django?", "course": self.course.id}
        request = self.generate_request(reverse('create-question'), self.post, data)
        response = views.create_question(request)
        assert response.status_code == 200
        assert response.data['status_code'] == 1

    def test_get_all_question(self):
        request = self.generate_request(reverse("question-by-course", kwargs={"course_id": self.course.id}))
        response = views.get_all_questions(request, self.course.id)
        assert response.status_code == 200
        assert response.data["data"] != {}

    def test_get_question_by_id(self):
        request = self.generate_request(reverse("question", kwargs={"id": self.question.id}))
        response = views.get_question_by_id(request, self.question.id)
        assert response.status_code == 200
        assert response.data["status_message"] == "Data Fetched"

    def test_update_question(self):
        data = {"question": "Why django?"}
        request = self.generate_request(reverse("update-question", kwargs={"question_id": self.question.id}), self.put, data)
        response = views.update_question(request, self.question.id)
        assert response.status_code == 200
        assert response.data["status_message"] == "Question successfully updated"
