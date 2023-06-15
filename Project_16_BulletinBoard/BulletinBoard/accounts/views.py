from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from accounts.forms import *


class ViewSignUp(CreateView):
    print("ViewSignUp")
    model = User
    form_class = CustomSignUpForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'