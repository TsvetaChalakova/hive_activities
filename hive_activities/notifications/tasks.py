from celery import shared_task
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


@shared_task(bind=True, max_retries=3)
def send_note_email_notification(self, recipient_data, note_data, activity_data, project_data, creator_data):

    try:
        domain = Site.objects.get_current().domain

        if not domain:
            domain = 'localhost:8000'

        context = {
            'recipient': recipient_data,
            'note': note_data,
            'activity': activity_data,
            'project': project_data,
            'created_by': creator_data,
            'domain': domain
        }

        email_subject = render_to_string(
            'notifications/email/note_notification_subject.txt',
            context
        ).strip()

        email_body = render_to_string(
            'notifications/email/note_notification_body.txt',
            context
        )

        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_data['email']],
            fail_silently=False
        )

        return "Email sent successfully"

    except Exception as exc:
        print(f"Failed to send email: {exc}")
        self.retry(exc=exc, countdown=60)
