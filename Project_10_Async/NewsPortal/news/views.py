import os
import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from news.filters import PostFilter
from news.forms import PostForm
from news.models import Post

from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from news.models import Subscription, Category

from django.http import HttpResponse
from django.views import View
from news.tasks import (
    hello,
    printer
)

from news.tasks import send_notify_new_post


class IndexView(View):
    def get(self, request):
        printer.apply_async(
            [15],
            eta=datetime.datetime.now() + datetime.timedelta(seconds=5)
        )
        hello.delay()
        return HttpResponse('Hello!')


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-post_create_datetime'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = os.path.join(
        "flatpages",
        'news_post.html'
    )
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    def get_queryset(self):

        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(
                self.request.GET,
                queryset
            )
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsListSearch(ListView):
    model = Post
    ordering = 'id'
    template_name = os.path.join(
        "flatpages",
        'post_search.html'
    )
    context_object_name = 'news_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(
                self.request.GET,
                queryset
            )
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsView(DetailView):
    model = Post
    ordering = "id"
    template_name = os.path.join(
        "flatpages",
        "news_view.html"
    )
    context_object_name = 'news_one'


class PostCreateNews(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    permission_required = (
        'news.add_post'
    )

    raise_exception = True

    form_class = PostForm
    model = Post
    template_name = os.path.join(
        "flatpages",
        "post_edit.html"
    )

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = "N"
        post.save()

        send_notify_new_post.apply_async([post.pk])

        return super().form_valid(form)


class PostCreateArticles(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    permission_required = (
        'news.add_post'
    )

    raise_exception = True

    form_class = PostForm
    model = Post
    template_name = os.path.join(
        "flatpages",
        "post_edit.html"
    )

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = "A"
        post.save()

        send_notify_new_post.apply_async([post.pk])

        return super().form_valid(form)


class PostUpdate(
    PermissionRequiredMixin,
    UpdateView
):
    permission_required = (
        'news.change_post'
    )

    form_class = PostForm
    model = Post
    template_name = os.path.join(
        "flatpages",
        "post_edit.html"
    )

class PostDelete(
    PermissionRequiredMixin,
    DeleteView
):
    permission_required = (
        'news.delete_post'
    )

    model=Post
    template_name = os.path.join(
        "flatpages",
        "post_delete.html"
    )
    success_url = reverse_lazy("news_list")


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category_name')

    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )