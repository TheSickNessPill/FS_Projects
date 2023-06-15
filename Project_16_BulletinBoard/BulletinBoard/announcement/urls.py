from django.urls import path
from announcement.views import *


urlpatterns = [
    path('', ViewAnnouncement.as_view(), name="announcement_list"),

    path('create/', ViewAnnouncementCreate.as_view()),

    path('<int:pk>', ViewAnnouncementDetail.as_view(), name="announsement"),
    path('<int:pk>/create_response', ViewAnnouncementResponseCreate.as_view(), name="announsement_create"),
    path('<int:pk>/edit', ViewAnnouncementEdit.as_view(), name="announsement_edit"),

    path('responsestome/', ViewAnnouncementResponse.as_view(), name="responsestome"),
    path('responsestome/<int:pk>/delete', ViewAnnouncementResponseDelete.as_view(), name="announsement_delete"),
    path('responsestome/<int:pk>/accept', ViewAnnouncementResponseAccept.as_view(), name="announsement_accept"),

    path('responsetome/<int:pk>', ViewAnnouncementResponseDetail.as_view(), name="responsetome"),

    path('subscriptions/', announcement_subscriptions, name='subscriptions')
]