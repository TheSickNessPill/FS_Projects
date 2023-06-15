from django.urls import path
from accounts.views import ViewSignUp


urlpatterns = [
    path('signup/', ViewSignUp.as_view(), name='viewsignup'),
]