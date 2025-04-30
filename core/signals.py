from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Answer

@receiver(post_save, sender=Answer)
def notify_question_author(sender, instance, created, **kwargs):
    if created:
        question = instance.question
        author_email = question.author.email
        send_mail(
            subject='New Answer to Your Question',
            message=f'Your question "{question.title}" has a new answer.',
            from_email='no-reply@example.com',
            recipient_list=[author_email],
        )
