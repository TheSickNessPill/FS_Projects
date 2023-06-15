from django.contrib import admin
from announcement.models import *

admin.site.register(Announcement)
admin.site.register(AnnouncementResponse)
admin.site.register(AnnouncementCategory)