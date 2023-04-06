from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from accounts.models import Author
from django.contrib.auth.models import User

from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(
        max_length=100,
        unique = True
    )

    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    article = "A"
    news = "N"

    POST_TYPES_LIST = [
        (article, "Article"),
        (news, "News")
    ]

    post_type = models.CharField(
        max_length=1,
        choices=POST_TYPES_LIST
    )
    post_create_datetime = models.DateTimeField(
        auto_now_add=True
    )
    post_title = models.CharField(
        max_length=255,
        default="No post_title"
    )
    post_text = models.TextField(
        default="No post_text"
    )
    post_rating = models.IntegerField(
        default=0
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        null=True
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='products',
        null=True
    )
    post_category = models.ManyToManyField(
        Category,
        through="PostCategory"
    )

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f"{self.post_text[:124]}..."

    def get_absolute_url(self):
        return reverse(
            "news_detail",
            args=[str(self.id)]
        )

    def __str__(self):
        return f'{self.post_title}. {self.post_type} .{self.post_create_datetime}'


class PostCategory(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    post_categoty = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True
    )


class Comment(models.Model):
    comment_text = models.TextField()
    comment_datetime = models.DateTimeField(
        auto_now_add=True
    )
    comment_rating = models.IntegerField(
        default=0
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    category = models.ForeignKey(
        to="Category",
        on_delete=models.CASCADE,
        related_name="subscription"
    )