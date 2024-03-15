from random import randint
from django.utils import timezone
from app.services.email_service import send_email
from django.conf import settings
from django.template.loader import render_to_string


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