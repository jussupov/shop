from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from celery import shared_task
import uuid
import requests
from requests.auth import HTTPBasicAuth
from shop import settings


@shared_task()
def email(to_email, code):
    subject = "Регистрация на сайте onlineshop.kz"

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [
        to_email,
    ]
    text_content = f"Welcome code is {code}."
    html_content = f"<p>Welcome code is <strong>{code}</strong>.</p>"
    print("hello")
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


merchant_id = settings.MERCHANT_ID
income_secret_key = settings.INCOME_SECRET_KEY

auth = HTTPBasicAuth(merchant_id, income_secret_key)
payment_url = settings.PAY_BOX_URL


def make_uuid():
    return str(uuid.uuid4())


def get_payment_details(id):
    return requests.get(f"{payment_url}/{id}", auth=auth)


class Payment:
    def __init__(self, amount, currency, description, order):
        self.currency = currency
        self.order = order
        self.amount = amount
        self.description = description

    def get_body(self):
        body = {
            "currency": "KZT",
            "order": self.order,
            "amount": self.amount,
            "description": self.description,
        }
        return body

    def create_payment(self):
        body = self.get_body()
        headers = {"X-Idempotency-Key": make_uuid()}
        r = requests.post(payment_url, json=body, auth=auth, headers=headers)
        print(r.content)
        return r
