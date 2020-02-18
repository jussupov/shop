from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from celery import shared_task


@shared_task()
def email(to_email, code):
    subject = "Регистрация на сайте onlineshop.kz"

    from_email = "support@onlineshop.kz"
    recipient_list = [
        to_email,
    ]
    text_content = f"Welcome code is {code}."
    html_content = f"<p>Welcome code is <strong>{code}</strong>.</p>"
    print("hello")
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

