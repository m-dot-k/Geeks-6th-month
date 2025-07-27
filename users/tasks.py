from celery import shared_task
from django.core.mail import send_mail
import time

@shared_task
def send_otp_email(user_email, code):
    print("Sending...")
    time.sleep(20)
    print ("Email sent")

@shared_task
def send_daily_report():
    print ("sending daily report...")
    time.sleep(50)
    print ("daily report sent")

@shared_task
def send_email(email):
    subject = "SPAM"
    message = "Это сообщение является спамом, проигнорируйте его"
    from_email = None
    recipient_list = ["python3workmail@gmail.com"]

    send_mail(subject, message, from_email, recipient_list)
