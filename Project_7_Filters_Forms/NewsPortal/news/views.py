import os

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


class PostCreateNews(CreateView):
    form_class = PostForm
    model = Post
    template_name = os.path.join(
        "flatpages",
        "post_edit.html"
    )

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = "N"
        return super().form_valid(form)


class PostCreateArticles(CreateView):
    form_class = PostForm
    model = Post
    template_name = os.path.join(
        "flatpages",
        "post_edit.html"
    )

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = "A"
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = os.path.join(
        "flatpages",
        "post_edit.html"
    )

class PostDelete(DeleteView):
    model=Post
    template_name = os.path.join(
        "flatpages",
        "post_delete.html"
    )
    success_url = reverse_lazy("news_list")