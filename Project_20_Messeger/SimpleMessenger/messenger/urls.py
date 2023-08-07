from django.urls import path
from messenger.views import *

urlpatterns = [
    path("", messanger_main, name="chats_viewer"),

    path("createdialog/", create_dialog, name="create_dialog"),
    path("deletedialog/", delete_dialog, name="delete_dialog"),

    path("createchat/", create_chat, name="create_chat"),
    path("editchat/", edit_chat, name="create_chat"),
    path("deletechat/", delete_chat, name="create_chat"),

    path("sendchattext/", send_chat_text, name="send_chat_text"),
    path("senddialogtext/", send_dialog_text, name="send_dialog_text"),

    path("allusers/", AllUsersView.as_view(), name="all_users_view")
]