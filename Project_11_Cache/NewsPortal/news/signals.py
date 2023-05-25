from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import EmailMultiAlternatives

from django.contrib.auth.models import User
from news.models import Post

@receiver(post_save, sender=Post)
def product_created(instance, created, **kwargs):
    if not created:
        return

    print(f"asdasd : || {instance.category} ")

    emails = User.objects.filter(
        subscriptions__category = instance.category
    ).values_list('email', flat=True)

    subject = f'Новая новость в категории {instance.category}'

    text_content = (
        f'Заголовок: {instance.post_title}\n'
        f'Дата: {instance.post_create_datetime}\n\n'
        f'Ссылка на Новость: http://127.0.0.1{instance.get_absolute_url()}'
    )

    html_content = (
        f'Заголовок: {instance.post_title}<br>'
        f'Дата: {instance.post_create_datetime}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
            'Ссылка на Новость'
        f'</a>'
    )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
