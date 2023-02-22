# import os
#
# from celery import Celery
# from fastapi import BackgroundTasks, Depends
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
#
# from app.api.endpoints.auth.router import current_user
# from app.config import SMTP_PASSWORD, SMTP_USER, SMTP_TO_USER
#
# SMTP_HOST = "smtp.gmail.com"
# SMTP_PORT = 587
#
# celery = Celery('tasks', broker='redis://localhost:6379')
#
#
# class Envs:
#     MAIL_USERNAME = SMTP_USER
#     MAIL_PASSWORD = SMTP_PASSWORD
#     MAIL_FROM = SMTP_TO_USER
#     MAIL_PORT = SMTP_PORT
#     MAIL_SERVER = SMTP_HOST
#     MAIL_FROM_NAME = 'danyanara'
#
#
# conf = ConnectionConfig(
#     MAIL_USERNAME=Envs.MAIL_USERNAME,
#     MAIL_PASSWORD=Envs.MAIL_PASSWORD,
#     MAIL_FROM=Envs.MAIL_FROM,
#     MAIL_PORT=Envs.MAIL_PORT,
#     MAIL_SERVER=Envs.MAIL_SERVER,
#     MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
#     MAIL_TLS=True,
#     MAIL_SSL=False,
#     USE_CREDENTIALS=True,
#     TEMPLATE_FOLDER='app/api/endpoints/templates/email'
# )
#
#
# async def send_email_async(subject: str, email_to: str, body: dict):
#     message = MessageSchema(
#         subject=subject,
#         recipients=[email_to],
#         body=body,
#         subtype='html',
#     )
#
#     fm = FastMail(conf)
#
#     await fm.send_message(message, template_name='email.html')
