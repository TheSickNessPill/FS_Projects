from django.views.decorators.cache import cache_page

from rest_framework import routers

from django.urls import path, include
from django.http import HttpResponse

from news.views import (
    NewsList,
    NewsListSearch,
    NewsView,
    PostCreateArticles,
    PostCreateNews,
    PostUpdate,
    PostDelete,

    IndexView,
    TestTransl,
    subscriptions
)

def multiply(request):
   number = request.GET.get('number')
   multiplier = request.GET.get('multiplier')

   try:
       result = int(number) * int(multiplier)
       html = f"<html><body>{number}*{multiplier}={result}</body></html>"
   except (ValueError, TypeError):
       html = f"<html><body>Invalid input.</body></html>"

   return HttpResponse(html)


urlpatterns = [
    path('multiply/', multiply),
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', cache_page(60 * 1)(NewsList.as_view()), name="news_list"),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    # path('<int:pk>', ProductDetail.as_view()),
    path("<int:pk>", cache_page(60 * 5)(NewsView.as_view()), name="news_detail"),

    path("news/create/", PostCreateNews.as_view(), name="news_create"),
    path("news/<int:pk>/edit/", PostUpdate.as_view(), name="news_update"),
    path("news/<int:pk>/delete/", PostDelete.as_view(), name="news_delete"),

    path("articles/create/", PostCreateArticles.as_view(), name="article_create"),
    path("articles/<int:pk>/edit/", PostUpdate.as_view(), name="article_update"),
    path("articles/<int:pk>/delete/", PostDelete.as_view(), name="article_delete"),

    path('<int:pk>/edit/', PostUpdate.as_view(), name="post_update"),
    path('<int:pk>/delete/', PostDelete.as_view(), name="post_delete"),

    path('search/', NewsListSearch.as_view(), name="post_search"),

    path('subscriptions/', subscriptions, name="subscriptions"),

    path('index/', IndexView.as_view()),

    path('test_transl/', TestTransl.as_view()),
]