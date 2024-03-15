from django.core.mail import EmailMultiAlternatives
from random import randint
from django.utils import timezone
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string

def send_email(subject, old_body, receiver):
    sender = settings.EMAIL_HOST_USER
    body = strip_tags(old_body)
    email = EmailMultiAlternatives(subject, body, sender, receiver)
    email.attach_alternative(old_body, "text/html")    
    email.fail_silently = True
    email.send()


def send_otp_mail(user):
    generated_otp = "".join([str(randint(0,9)) for _ in range(0, 6) ])
    user.otp = generated_otp
    user.otp_sent_date = timezone.now()
    user.save()
    body = render_to_string("otp_email.html", context={"otp": generated_otp})
    send_email(
        "OTP Verification",
        body,
        [user.email]
    )