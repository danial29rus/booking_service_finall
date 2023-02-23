# import ssl
#
# from celery import Celery
# import smtplib
# from email.message import EmailMessage
#
# from fastapi import Depends
# from app.api.endpoints.auth.utils import get_current_user
# from app.config import SMTP_PASSWORD, SMTP_USER, SMTP_TO_USER
#
# SMTP_HOST = "smtp.gmail.com"
# SMTP_PORT = 465
#
# celery = Celery('tasks', broker='redis://localhost:6379')
#
#
# def get_email_template_dashboard(email_to: str):
#     email = EmailMessage()
#     email['Subject'] = 'Натрейдил Отчет Дашборд'
#     email['From'] = SMTP_USER
#     email['To'] = email_to
#
#     email.set_content(f"Здравствуйте, {email_to}, вы забронировали отель !")
#     return email
#
#
# @celery.task
# def send_email_report_dashboard(email_to: str):
#     email = get_email_template_dashboard(email_to)
#     with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
#         server.login(SMTP_USER, SMTP_PASSWORD)
#         server.send_message(email)
