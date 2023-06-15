from django import forms
from django.db import models
from announcement.models import *

class FormAnnouncement(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            "title",
            "text",
            "attachment",
            "category",
        ]


class FormResponce(forms.ModelForm):
    class Meta:
        model = AnnouncementResponse
        fields = [
            "text",
        ]


class FormResponceAccept(forms.ModelForm):
    class Meta:
        model = AnnouncementResponse
        fields = [
            "is_accepted"
        ]