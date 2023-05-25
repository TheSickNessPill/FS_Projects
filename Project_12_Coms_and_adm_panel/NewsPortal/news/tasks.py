from celery import shared_task
import time
import datetime

from django.core.mail import (
    mail_managers,
    send_mail
)
from news.models import (
    Post,
    Category,
    Subscription
)
from django.contrib.auth.models import User

from django.core.mail import EmailMultiAlternatives

@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)


# Реализовать еженедельную рассылку с последними новостями (каждый понедельник в 8:00 утра)
@shared_task
def send_last_week_news():
    categoryes = Category.objects.filter()

    previous_week_datetime = datetime.datetime.now() - datetime.timedelta(days=7, minutes=1)

    for category in categoryes:
        category_posts = Post.objects.filter(category)
        category_posts = filter(
            lambda post:
                post.post_create_datetime > previous_week_datetime,
            category_posts
        )
        category_posts = "\n".join(
            ["{} - {}".format(post.post_title, post.get_absolute_url()) for post in category_posts]
        )
        category_subs = Subscription.objects.filter(category_id=category)
        category_subs = [User.objects.filter(id=sub.user_id)[0].email for sub in category_subs]

        send_mail(
            subject='Список Новостей',
            message=category_posts,
            from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
            recipient_list=category_subs,
        )


# Реализовать рассылку уведомлений подписчикам после создания новости.
@shared_task
def send_notify_new_post(new_post_id):
    new_post = Post.objects.filter(pk=new_post_id)

    emails = User.objects.filter(
        subscriptions__category = new_post.category
    ).values_list('email', flat=True)

    subject = f'Новая новость в категории {new_post.category}'

    text_content = (
        f'Заголовок: {new_post.post_title}\n'
        f'Дата: {new_post.post_create_datetime}\n\n'
        f'Ссылка на Новость: http://127.0.0.1{new_post.get_absolute_url()}'
    )

    html_content = (
        f'Заголовок: {new_post.post_title}<br>'
        f'Дата: {new_post.post_create_datetime}<br><br>'
        f'<a href="http://127.0.0.1{new_post.get_absolute_url()}">'
            'Ссылка на Новость'
        f'</a>'
    )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()