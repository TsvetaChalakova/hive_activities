from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_welcome_email(user_email, first_name, last_name):
    subject = "Welcome to Hive Activities"
    message = (f"Hi {first_name} {last_name},\n"
               f"\nWelcome to Hive Activities! We're excited to have you on board. "
               f"Feel free to explore and let us know if you have any questions.\n"
               f"\nBest regards,"
               f"\nHive Activities Team")
    from_email = "hive.activities.notifs@gmail.com"
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)