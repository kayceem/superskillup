from django.core.mail import EmailMultiAlternatives
from random import randint
from django.utils import timezone
from django.conf import settings
from django.utils.html import strip_tags

def send_email(subject, old_body, receiver):
    sender = settings.EMAIL_HOST_USER
    body = strip_tags(old_body)
    email = EmailMultiAlternatives(subject, body, sender, receiver)
    email.attach_alternative(old_body, "text/html")    
    email.fail_silently = True
    email.send()

