from django.urls import path
from news.views import NewsList, NewsView
from news.views import (
    NewsList,
    NewsListSearch,
    NewsView,
    PostCreateArticles,
    PostCreateNews,
    PostUpdate,
    PostDelete
)


urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', NewsList.as_view(), name="news_list"),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    # path('<int:pk>', ProductDetail.as_view()),
    path("<int:pk>", NewsView.as_view(), name="news_detail"),

    path("news/create/", PostCreateNews.as_view(), name="news_create"),
    path("news/<int:pk>/edit/", PostUpdate.as_view(), name="news_update"),
    path("news/<int:pk>/delete/", PostDelete.as_view(), name="news_delete"),

    path("articles/create/", PostCreateArticles.as_view(), name="article_create"),
    path("articles/<int:pk>/edit/", PostUpdate.as_view(), name="article_update"),
    path("articles/<int:pk>/delete/", PostDelete.as_view(), name="article_delete"),

    path('<int:pk>/edit/', PostUpdate.as_view(), name="post_update"),
    path('<int:pk>/delete/', PostDelete.as_view(), name="post_delete"),

    path('search/', NewsListSearch.as_view(), name="post_search")
]