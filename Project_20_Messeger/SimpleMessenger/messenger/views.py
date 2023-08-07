import json
import random

from django.shortcuts import render
from django.views.generic import ListView, CreateView
from messenger.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.http import QueryDict

class AllUsersView(ListView):
    model = User
    ordering = "username"
    template_name = "all_users_list.html"
    context_object_name = "allusers"
    paginate_by = 50


@login_required
@csrf_protect
def messanger_main(request):
    if request.method == 'GET':
        print(request.path)
        chat_messages = []
        dialog_messages = []
        dialog_name = None
        chat_name = None


        if request.GET.get("dialog_name"):
            print(request.GET)
            dialog_name = request.GET.get("dialog_name")
            print("dialog_name", dialog_name)
            dialog_another_user = User.objects.filter(username=dialog_name)[0]


            another_user = User.objects.filter(username=dialog_another_user)[0]
            another_user_dialogs = Dialog.objects.filter(member=another_user).values("id_number")
            another_user_dialogs = list(map(lambda x: x.get("id_number"), another_user_dialogs))

            current_user_dialogs = Dialog.objects.filter(member=request.user).values("id_number")
            current_user_dialogs = list(map(lambda x: x.get("id_number"), current_user_dialogs))

            dialog_id = set(another_user_dialogs).intersection(set(current_user_dialogs))
            dialog_id = list(dialog_id)[0]

            dialog = Dialog.objects.filter(id_number=dialog_id)[0]

            dialog_messages = DialogMessages.objects.filter(dialog=dialog)
            if dialog_messages:
                dialog_messages = [
                    [
                        dialog_message.message.from_user,
                        dialog_message.message.text,
                        dialog_message.message.create_date
                    ]
                        for dialog_message in dialog_messages
                ]
            else:
                dialog_messages = []

            print("dialog_another_messages", dialog_messages)


            if dialog_messages:
                dialog_messages = sorted(dialog_messages, key=lambda x: x[2])

            print("dialog_messages", dialog_messages)

        elif request.GET.get("chat_name"):
            print(request.GET)
            chat_name = request.GET.get("chat_name")
            chat = Chat.objects.filter(chat_name=chat_name, is_creater=True)[0]
            chat_messages = ChatMessages.objects.filter(chat=chat)
            if chat_messages:
                chat_messages = [
                    [
                        chat_message.message.from_user,
                        chat_message.message.text,
                        chat_message.message.create_date.strftime("%Y-%m-%d %H:%M:%S")
                    ]
                        for chat_message in chat_messages
                ]

        current_user = request.user
        ids_list = Dialog.objects.filter(member=current_user).values("id_number")
        ids_list = [id.get("id_number") for id in ids_list]

        dialog_list = Dialog.objects.filter(id_number__in=ids_list).exclude(member=current_user)
        chat_list = Chat.objects.all().values("chat_name").distinct()

    return render(
        request,
        'start_page.html',
        {
            "dialog_list": dialog_list,
            "dialog_messages": dialog_messages,
            "dialog_name": dialog_name,

            "chat_list": chat_list,
            "chat_messages": chat_messages,
            "chat_name": chat_name,
        }
    )


@login_required
@csrf_protect
def create_dialog(request):
    if request.method == "GET":
        another_username = request.GET["another_username"]
        another_user = User.objects.filter(username=another_username)
        if another_user:
            another_user = another_user[0]
        else:
            return JsonResponse({
                "status": "error",
                "errortext": "username do not exists"
            })

        current_user = request.user

        if current_user == another_user:
            return JsonResponse({
                "status": "error",
                "errortext": "You can not create dialog with yourself"
            })

        current_username_dialogs = Dialog.objects.filter(member=current_user)
        current_username_dialogs = [dialog.id_number for dialog in current_username_dialogs]
        current_username_dialogs = set(current_username_dialogs)

        another_username_dialogs = Dialog.objects.filter(member=another_user)
        another_username_dialogs = [dialog.id_number for dialog in another_username_dialogs]
        another_username_dialogs = set(another_username_dialogs)

        if current_username_dialogs.intersection(another_username_dialogs):
            return JsonResponse({
                "status": "error",
                "errortext": "dialog already exists"
            })

        quantity = len(Dialog.objects.all())
        if not quantity:
            quantity = 1
        else:
            quantity = quantity // 2 + 1

        Dialog.objects.create(id_number=quantity, member=another_user)
        Dialog.objects.create(id_number=quantity, member=current_user)

    return JsonResponse({
        "status": "ok",
        "dialogname": another_user.username
    })


@login_required
@csrf_protect
def delete_dialog(request):
    if request.method == "GET":
        another_username = request.GET["username"]
        print("delete_dialog", another_username)

        another_user = User.objects.filter(username=another_username)

        if not another_user:
            return JsonResponse({
                "status": "error",
                "errortext": "user do not exists"
            })
        another_user = another_user[0]

        current_user = request.user

        print("another_user", another_user)
        print("current_user", current_user)

        if current_user == another_user:
            return JsonResponse({
                "status": "error",
                "errortext": "You should set another username, not yourself"
            })

        current_username_dialogs = Dialog.objects.filter(member=current_user)
        current_username_dialogs = [dialog.id_number for dialog in current_username_dialogs]
        current_username_dialogs = set(current_username_dialogs)


        another_username_dialogs = Dialog.objects.filter(member=another_user)
        another_username_dialogs = [dialog.id_number for dialog in another_username_dialogs]
        another_username_dialogs = set(another_username_dialogs)

        dialog_id = current_username_dialogs.intersection(another_username_dialogs)
        dialog_id = list(dialog_id)[0]
        print("dialog_id", dialog_id)

        if dialog_id:
            dialog = Dialog.objects.filter(id_number=dialog_id)
            if dialog:
                dialog.delete()

            return JsonResponse({
                "status": "ok",
                "dialogname": another_user.username
            })

        else:
            return JsonResponse({
                "status": "error",
                "errortext": "Dialog do not exists"
            })


@login_required
@csrf_protect
def create_chat(request):
    if request.method == "GET":
        chatname = request.GET["chatname"]
        usernames = request.GET["usernames"]
        print("chatname", chatname)

        usernames = usernames.strip().split(" ")
        usernames = [username.strip() for username in usernames]
        print("usernames", usernames)

        if request.user.username in usernames:
            return JsonResponse({
                "status": "error",
                "errortext": "You should set another usernames, not yourself"
            })

        users_result = [User.objects.filter(username=username) for username in usernames]
        print("users_result", users_result)
        if not all(users_result):
            return JsonResponse({
                "status": "error",
                "errortext": "Not all scesified users are exists"
            })

        usernames.append(request.user.username)

        for username in usernames:
            user_obj = User.objects.filter(username=username)[0]
            if username == request.user.username:
                Chat.objects.create(chat_name=chatname, member=user_obj, is_creater=True)
            else:
                Chat.objects.create(chat_name=chatname, member=user_obj, is_creater=False)

    return JsonResponse({
        "status": "ok",
        "chatname": chatname
    })


@login_required
@csrf_protect
def edit_chat(request):
    if request.method == "GET":
        current_user = request.user
        current_username = request.user.username
        current_chat_name = request.GET["chatname"]
        new_chat_name = request.GET["newchatname"]

        print("current_user", current_user)
        print("current_username", current_username)
        print("current_chat_name", current_chat_name)
        print("new_chat_name", new_chat_name)

        chat = Chat.objects.filter(chat_name=current_chat_name, member=current_user)
        if not chat:
            return JsonResponse({
                "status": "error",
                "errortext": "chat do not exists or you are not member of this chat"
            })

        chat = chat[0]
        if not chat.is_creater:
            return JsonResponse({
                "status": "error",
                "errortext": "you are not creator of this chat to delete him"
            })

        current_chat = Chat.objects.filter(chat_name=current_chat_name)
        for chat_row in current_chat:
            chat_row.chat_name = new_chat_name
            chat_row.save()


    return JsonResponse({
        "status": "ok",
        "newchatname": new_chat_name
    })


@login_required
@csrf_protect
def delete_chat(request):
    if request.method == "GET":
        current_user = request.user
        current_username = request.user.username
        current_chat_name = request.GET["chatname"]

        chat = Chat.objects.filter(chat_name=current_chat_name, member=current_user)
        if not chat:
            return JsonResponse({
                "status": "error",
                "errortext": "chat that you trying to delete do not exists or you are not member of this chat"
            })

        chat = chat[0]
        if not chat.is_creater:
             return JsonResponse({
                "status": "error",
                "errortext": "you can't delete this chat because you are not creater of this chat"
            })

        Chat.objects.filter(chat_name=current_chat_name).delete()

    return JsonResponse({
        "status": "ok",
        "chatname": current_chat_name
    })


@login_required
@csrf_protect
def send_chat_text(request):
    if request.method == "GET":
        print(request.GET["text"])
        print(request.GET["name"])

        new_message = Message.objects.create(text=request.GET["text"], from_user=request.user)
        time = new_message.create_date.strftime("%Y-%m-%d %H:%M:%S")

        chat = Chat.objects.filter(chat_name=request.GET["name"], is_creater=True)[0]
        ChatMessages.objects.create(chat=chat, message=new_message)


    return JsonResponse({
        "status": "ok",
        "text": request.GET["text"],
        "user": request.user.username,
        "chat": request.GET["name"],
        "time": time
    })


@login_required
@csrf_protect
def send_dialog_text(request):
    if request.method == "GET":
        text = request.GET["text"]
        print(text)
        another_username = request.GET["name"]
        print(another_username)

        new_message = Message.objects.create(text=text, from_user=request.user)
        time = new_message.create_date.strftime("%Y-%m-%d %H:%M:%S")

        another_user = User.objects.filter(username=another_username)[0]
        another_user_dialogs = Dialog.objects.filter(member=another_user).values("id_number")
        another_user_dialogs = list(map(lambda x: x.get("id_number"), another_user_dialogs))

        current_user_dialogs = Dialog.objects.filter(member=request.user).values("id_number")
        current_user_dialogs = list(map(lambda x: x.get("id_number"), current_user_dialogs))

        dialog_id = set(another_user_dialogs).intersection(set(current_user_dialogs))
        dialog_id = list(dialog_id)[0]

        dialog = Dialog.objects.filter(id_number=dialog_id)[0]
        print("dialog", dialog)
        DialogMessages.objects.create(dialog=dialog, message=new_message)


    return JsonResponse({
        "status": "ok",
        "text": text,
        "user": request.user.username,
        "chat": another_username,
        "time": time
    })