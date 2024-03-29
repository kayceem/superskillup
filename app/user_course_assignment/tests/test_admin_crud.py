from rest_framework.test import force_authenticate
from django.test import TestCase, RequestFactory
from django.urls import reverse
from app.user_course_assignment import admin_views
from app.models import Course, UserProfile, UserCourseAssignment
from django.contrib.auth.models import User


class TestAdminUserAssignment(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.user = UserProfile.objects.create(name='testuser', email='testuser@ramailo.tech', password='password123', is_verified=True)
        self.admin = User.objects.create(username="admin", email="admin@gmail.com", password="admin123")
        self.course = Course.objects.create(name="Test Course 1")
        self.course_unassigned = Course.objects.create(name="Test Course 2")
        self.assign = UserCourseAssignment.objects.create(course=self.course, user=self.user, assigned_by=self.admin)
        self.post = 'post'
        self.get = 'get'
        self.put = 'put'

    def generate_request(self, url, method='get', data=None):
        content_type = 'application/json'
        if method == self.post:
            request = self.request.post(path=url, data=data, content_type=content_type)
        if method == self.get:
            request = self.request.get(url)
        if method == self.put:
            request = self.request.put(url, data, content_type)
        force_authenticate(request, user=self.admin)
        return request

    def test_assign_course(self):
        data = {"course": self.course_unassigned.id, "user": self.user.id}
        request = self.generate_request(reverse("admin-assign-course"), self.post, data)
        response = admin_views.assign_course(request)
        assert response.status_code == 200
        assert response.data["status_message"] == "Course Assigned Successfully"
        assert response.data["data"]["course"] == self.course_unassigned.id

    def test_update_assign_course(self):
        data = {"course": self.course.id, "user": self.user.id}
        request = self.generate_request(reverse("admin-update-assign-course", kwargs={'id': self.assign.id}), self.put, data)
        response = admin_views.update_assigned_course(request, self.assign.id)
        assert response.status_code == 200
        assert response.data["status_message"] == "Successfully updated"
        assert response.data["data"]["course"] == self.course.id

    def test_get_all_assignments(self):
        request = self.generate_request(reverse("admin-assignments"))
        response = admin_views.get_all_assignments(request)
        assert response.status_code == 200
        assert response.data["data"][0]["course"] == self.course.id

    def test_get_assignment_by_id(self):
        request = self.generate_request(reverse('admin-assignment-by-id', kwargs={'id': self.assign.id}))
        response = admin_views.get_assignment_by_id(request, self.assign.id)
        assert response.status_code == 200
        assert response.data["data"]["id"] == self.assign.id

    def test_get_assignments_of_user(self):
        request = self.generate_request(reverse('admin-user-assignments', kwargs={'user_id': self.user.id}))
        response = admin_views.get_assignments_of_user(request, self.user.id)
        assert response.status_code == 200
        assert response.data["data"][0]["id"] == self.assign.id

    def test_get_user_assigned_courses(self):
        request = self.generate_request(reverse('admin-assigned-courses', kwargs={'user_id': self.user.id}))
        response = admin_views.get_user_assigned_courses(request, self.user.id)
        assert response.status_code == 200
        assert response.data["data"]["user"] == self.user.id
        # TODO :: change the reponse to send course dict instead of nested data dict
        assert response.data["data"]["data"][0]["id"] == self.course.id

    def test_get_assigned_topics(self):
        request = self.generate_request(reverse('admin-assigned-topics', kwargs={'assign_id': self.assign.id}))
        response = admin_views.get_assigned_topics(request, self.assign.id)
        assert response.status_code == 200
        # TODO :: change user email to id
        assert response.data["data"]["user"] == self.user.email
        assert 'topics' in response.data["data"]
