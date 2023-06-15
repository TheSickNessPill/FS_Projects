from django_filters import FilterSet
from announcement.models import *


class FilterAnnouncement(FilterSet):
    class Meta:
        model = Announcement
        fields = {
            'title': ['icontains'],
            'by_user': ['exact'],
            'create_time': ['lt', 'gt']
        }


class FilterAnnouncementResponse(FilterSet):
    class Meta:
        model = AnnouncementResponse
        fields = {
            'text': ['icontains'],
            'by_user': ['exact'],
            'create_time': ['lt', 'gt']
        }