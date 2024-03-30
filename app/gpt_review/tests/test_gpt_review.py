from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework.test import force_authenticate
from app.models import Course, Question, UserCourseAssignment, UserProfile, UserAnswer, GptReview
from django.contrib.auth.models import User
from app.user_answer import user_views as answer_views
from app.gpt_review import user_views as gpt_views


class TestQuestion(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.user = UserProfile.objects.create(name='testuser', email='testuser@ramailo.tech', password='password123')
        self.course = Course.objects.create(name="django")
        self.admin = User.objects.create_user(username='testadmin', email='test@ramailo.tech', password='password123')
        self.question1 = Question.objects.create(question="Question 1", course=self.course)
        self.question2 = Question.objects.create(question="Question 2", course=self.course)
        self.assign = UserCourseAssignment.objects.create(course=self.course, user=self.user, assigned_by=self.admin)
        self.answer = UserAnswer.objects.create(answer="yes", question=self.question2, user_course_assignment=self.assign)
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

    def test_add_gpt_review(self):
        data = {"user_course_assignment": self.assign.id, "question": self.question1.id, "answer": "Testing is a process of checking whether something is right or not."}
        request = self.generate_request(reverse('add-answer'), self.post, data)
        response = answer_views.add_answer(request)
        assert response.status_code == 200
        assert response.data['status_code'] == 1
        answer_id = response.data['data']['id']
        request = self.generate_request(reverse('admin-get-gpt-review-by-answer-id', kwargs={"answer_id": answer_id}))
        response = gpt_views.get_gpt_review_by_answer(request, answer_id)
        assert response.status_code == 200
        assert response.data['status_code'] == 1

    def test_update_gpt_review(self):
        data = {"answer": "Testing is a process of checking whether something is right or not."}
        request = self.generate_request(reverse('update-answer', kwargs={"id": self.answer.id}), self.put, data)
        response = answer_views.update_answer(request, self.answer.id)
        assert response.status_code == 200
        assert response.data['status_code'] == 1
        request = self.generate_request(reverse('user-get-gpt-review-by-answer-id', kwargs={"answer_id": self.answer.id}))
        assert response.status_code == 200
        assert response.data['status_code'] == 1
