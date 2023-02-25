

import ssl

from celery import Celery
import smtplib
from email.message import EmailMessage

from fastapi import Depends
from app.api.endpoints.auth.utils import get_current_user
from app.config import SMTP_PASSWORD, SMTP_USER, SMTP_TO_USER,REDIS_PORT,REDIS_HOST

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:6379')


def get_email_template_dashboard(email_to: str, dateto, datofrom, hotelname, totalcost):
    email = EmailMessage()
    email['Subject'] = 'Booking Hotel'
    email['From'] = SMTP_USER
    email['To'] = email_to

    email.set_content(f"""Вы {email_to} забронировали номер в отеле {hotelname}. Период: с {datofrom} по {dateto}. К оплате {totalcost} RUB. """)
    return email


@celery.task
def send_email_report_dashboard(email_to: str, dateto, datofrom, hotelname, totalcost):
    email = get_email_template_dashboard(email_to, dateto, datofrom, hotelname, totalcost)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)