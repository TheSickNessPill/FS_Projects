from django import forms
import time

from allauth.account.forms import SignupForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.core.mail import send_mail
from django.core.mail import mail_managers
from django.core.mail import mail_admins
from django.core.mail import EmailMultiAlternatives

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="FirstName")
    last_name = forms.CharField(label="LastName")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="authors")
        user.groups.add(common_users)


        print("Status 11")

        subject = 'Добро пожаловать в новостной портал!'
        text = f'{user.username}, вы успешно зарегистрировались!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/news"> сайте </a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text,
            from_email=None,
            to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        print("Status 22")
        time.sleep(2)

        mail_managers(
            subject="Новый пользователь!",
            message=f"МЕНЕДЖЕР. Пользователь {user.username} зарегистрировался на сайте."
        )
        print("Status 33")
        time.sleep(2)

        mail_admins(
            subject='Новый пользователь!',
            message=f"ADMIN. 'Пользователь {user.username} зарегистрировался на сайте."
        )
        print("Status 44")



        # send_mail(
        #     subject='Добро пожаловать в новостной портал!',
        #     message=f'{user.username}, вы успешно зарегистрировались!',
        #     from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
        #     recipient_list=[user.email],
        # )


        return user