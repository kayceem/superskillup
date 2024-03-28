from rest_framework.test import force_authenticate
from django.test import TestCase, RequestFactory
from django.urls import reverse
from app.user_course_assignment import user_views
from app.user_course_assignment import admin_views
from app.models import Course, UserProfile, UserCourseAssignment
from django.contrib.auth.models import User


class TestAdminUserAssignment(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.user = UserProfile.objects.create(name='testuser', email='testuser@ramailo.tech', password='password123', is_verified=True)
        self.admin = User.objects.create(username="admin", email="admin@gmail.com", password="admin123")
        self.course = Course.objects.create(name="django")
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
        data = {"course": self.course.id, "user": self.user.id}
        request = self.generate_request(reverse("admin-assign-course"), self.post, data)
        response = admin_views.assign_course(request)
        print(response.data["error"])
        assert response.status_code == 200
        assert response.data["status_message"] == "Course Assigned Successfully"
        assert response.data["data"]["course"] == self.course.id

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
        assert response.data["data"] != {}
        assert response.data["data"][0]["course"] == self.course.id
