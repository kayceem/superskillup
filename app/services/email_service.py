from django.core.mail import EmailMultiAlternatives
from random import randint
from django.utils import timezone
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string

import logging


log = logging.getLogger(__name__)


def send_email(subject, body, receiver):
    sender = settings.EMAIL_HOST_USER
    email = EmailMultiAlternatives(subject, strip_tags(body), sender, receiver)
    email.attach_alternative(body, "text/html")
    email.fail_silently = True
    email.send()


def send_otp_mail(user):
    try:
        generated_otp = "".join([str(randint(0, 9)) for _ in range(0, 6)])
        user.otp = generated_otp
        user.otp_sent_date = timezone.now()
        user.save()
        body = render_to_string("otp_email.html", context={"otp": generated_otp})
        log.info(f"Sending OTP verification mail to: {user.email}")
        send_email("OTP Verification", body, [user.email])
    except Exception as e:
        log.error(f"Failed sending otp verification mail to: {user.email} - {str(e)}")


def send_course_enrolled_mail(enrollment):
    try:
        log.info(f"Sending course enrolled mail to: {enrollment.user.email}")
        body = render_to_string("course_assigned.html", context={"user": enrollment.user.name, "course": enrollment.course.name, "manager": enrollment.enrolled_by.username})
        send_email(f"Course: {enrollment.course.name}", body, [enrollment.user.email])
    except Exception as e:
        log.error(f"Failed sending course enrolled mail to: {enrollment.user.email} - {str(e)}")


def send_assignment_submitted_mail(user_assignment, user_assignment_submission):
    try:
        log.info(f"Sending assignment submitted mail to: {user_assignment.user_course_enrollment.enrolled_by.email}")
        context = {"user": user_assignment.user_course_enrollment.user.name, "admin": user_assignment.user_course_enrollment.enrolled_by.username, "assignment": user_assignment.assignment.title, "course": user_assignment.assignment.course.name, "description": user_assignment_submission.get('description', None), "url": user_assignment_submission.get('url', None), "file": user_assignment_submission.get('file', None)}
        body = render_to_string("assignment_submitted.html", context=context)
        subject = f"Assignment Submission - {user_assignment.assignment.title}"
        send_email(subject, body, [user_assignment.user_course_enrollment.enrolled_by.email])
    except Exception as e:
        log.error(f"Failed assignment submitted mail to: {user_assignment.user_course_enrollment.enrolled_by.email} - {str(e)}")


def send_assignment_assigned_mail(user_assignment):
    try:
        log.info(f"Sending assignment assigned mail to: {user_assignment.user_course_enrollment.user.email}")
        context = {"user": user_assignment.user_course_enrollment.user.name, "admin": user_assignment.user_course_enrollment.enrolled_by.username, "assignment": user_assignment.assignment.title, "course": user_assignment.assignment.course.name}
        body = render_to_string("assignment_assigned.html", context=context)
        subject = f"Assignment - {user_assignment.assignment.title}"
        send_email(subject, body, [user_assignment.user_course_enrollment.user.email])
    except Exception as e:
        log.error(f"Failed assignment assigned mail to: {user_assignment.user_course_enrollment.user.email} - {str(e)}")


def send_question_answer_reviewed_mail(manager_feedback):
    try:
        course_enrollment = manager_feedback.gpt_review.question_answer.user_course_enrollment
        question = manager_feedback.gpt_review.question_answer.question
        log.info(f"Sending question answer reviewed mail to: {course_enrollment.user.email}")
        context = {"user": course_enrollment.user.name, "admin": course_enrollment.enrolled_by.username, "course": course_enrollment.course.name, "question": question.question}
        body = render_to_string("question_reviewed.html", context=context)
        subject = f"Question Answer Reviewed - {question.question}"
        send_email(subject, body, [course_enrollment.user.email])
    except Exception as e:
        log.error(f"Failed question answer reviewed mail to: {course_enrollment.user.email} - {str(e)}")
