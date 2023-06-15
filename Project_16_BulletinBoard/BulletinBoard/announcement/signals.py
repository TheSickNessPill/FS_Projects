from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver

from announcement.models import *


@receiver(post_save, sender=Announcement)
def announcement_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__category=instance.category
    ).values_list('email', flat=True)

    subject = f'New announcent in category {instance.category}'

    text_content = (
        f'Title: {instance.title}\n'
        f'Category: {instance.category}\n\n'
        f'Link: http://127.0.0.1:8000/{instance.get_absolute_url()}'
    )
    html_content = (
        f'Title: {instance.title}<br>'
        f'Category: {instance.category}<br><br>'
        f'<a href="http://127.0.0.1:8000/{instance.get_absolute_url()}">'
        f' Announcement\'s Link </a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(post_save, sender=AnnouncementResponse)
def response_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        email=instance.announcement.by_user.email
    ).values_list('email', flat=True)

    subject = f'New response to your announcement. [{instance.id}]'

    text_content = (
        f'By_user: {instance.by_user.username}\n'
        f'Text: {instance.text[:30]}...\n\n'
        f'Link: http://127.0.0.1:8000/{instance.get_absolute_url()}'
    )
    html_content = (
        f'By_user: {instance.by_user.username}<br>'
        f'Text: {instance.text[:30]}...<br><br>'
        f'<a href="http://127.0.0.1:8000/{instance.get_absolute_url()}">'
        f' Link to response </a>'
    )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()