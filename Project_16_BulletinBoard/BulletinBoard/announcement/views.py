from django.urls import reverse_lazy
from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from announcement.models import *
from announcement.forms import *
from announcement.filters import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef

from django.core.mail import EmailMultiAlternatives


class ViewAnnouncement(ListView):
    model = Announcement
    ordering = "-id"
    template_name = "announcements.html"
    context_object_name = "announcements"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = FilterAnnouncement(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset

        return context


class ViewAnnouncementDetail(DetailView):
    model = Announcement
    template_name = "announcement.html"
    context_object_name = "announcement"


class ViewAnnouncementCreate(CreateView):
    form_class = FormAnnouncement
    model = Announcement
    template_name = "announcement_edit.html"

    def form_valid(self, form):
        announcement = form.save(commit=False)
        user_id = self.request.user.id
        user =  User.objects.filter(pk=user_id)[0]
        announcement.by_user = user

        announcement.save()

        return super().form_valid(form)

class ViewAnnouncementEdit(UpdateView):
    form_class = FormAnnouncement
    model = Announcement
    template_name = "announcement_edit.html"


class ViewAnnouncementResponse(LoginRequiredMixin, ListView):
    model = AnnouncementResponse
    ordering = "-id"
    template_name = "responsestome.html"
    context_object_name = "responsestome"
    paginate_by = 10

    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = FilterAnnouncementResponse(self.request.GET, queryset)

        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        responses = context.get("responsestome")
        user_id = self.request.user.id

        responses = list(filter(
            lambda x: x.announcement.by_user.id == user_id,
            responses
        ))

        context["responsestome"] = responses
        context['filterset'] = self.filterset

        return context


class ViewAnnouncementResponseDetail(LoginRequiredMixin, DetailView):
    model = AnnouncementResponse
    template_name = "responsetome.html"
    context_object_name = "responsetome"

    raise_exception = True


class ViewAnnouncementResponseCreate(CreateView):
    form_class = FormResponce
    model = AnnouncementResponse
    template_name = "response.html"

    def form_valid(self, form):
        response = form.save(commit=False)
        user_id = self.request.user.id
        user =  User.objects.filter(pk=user_id)[0]
        response.by_user = user

        announcement_id = self.request.path.split("/")[-2]
        announcement_id = int(announcement_id)
        announcement = Announcement.objects.filter(pk=announcement_id)[0]
        response.announcement = announcement

        return super().form_valid(form)


class ViewAnnouncementResponseDelete(DeleteView):
    model = AnnouncementResponse
    template_name = 'response_delete.html'
    context_object_name = "response"
    success_url = reverse_lazy('responsestome')


class ViewAnnouncementResponseAccept(UpdateView):
    form_class = FormResponceAccept
    model = AnnouncementResponse
    template_name = "response_accept.html"
    context_object_name ="responce"
    success_url = reverse_lazy('responsestome')

    def form_valid(self, form):
        response = form.save(commit=False)

        if form.is_valid() and response.is_accepted:
            announcement_title = response.announcement.title
            email = response.by_user.email
            username = response.by_user.username
            create_time = response.create_time

            subject = f'Your responce to announcement was accepted'

            text_content = (
                f'Announcement title: {announcement_title}\n'
                f'Created time: {create_time}\n'
                f'Text: {response.text[:30]}...\n\n'
                f'Link: http://127.0.0.1:8000/{response.get_absolute_url()}'
            )
            html_content = (
                f'Announcement title: {announcement_title}<br>'
                f'Created time: {create_time}<br>'
                f'Text: {response.text[:30]}...<br><br>'
                f'<a href="http://127.0.0.1:8000/{response.get_absolute_url()}">'
                f' Link to response </a>'
            )

            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        return super().form_valid(form)


@login_required
@csrf_protect
def announcement_subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = AnnouncementCategory.objects.get(id=category_id)

        action = request.POST.get('action')
        if action == 'subscribe':
            AnnouncementSubscription.objects.create(
                user=request.user,
                category=category
            )
        elif action == 'unsubscribe':
            AnnouncementSubscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = AnnouncementCategory.objects.annotate(
        user_subscribed=Exists(
            AnnouncementSubscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )