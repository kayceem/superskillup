from django.core.mail import send_mail
from random import randint
from django.utils import timezone

def send_otp_mail(author):
    generated_otp = "".join([str(randint(0,9)) for _ in range(0, 6) ])
    author.otp = generated_otp
    author.otp_sent_date = timezone.now()
    author.save()
    send_mail(
        "OTP Varification",
        f"Your otp for verification is {generated_otp}. Please verify as soon as possible. OTP is valid for 10 minutes only.",
        "tamangnaresh386@gmail.com",
        [author.email],
        fail_silently=True
    )
