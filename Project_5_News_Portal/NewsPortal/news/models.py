from django.db import models
from django.conf import settings
from accounts.models import Author

class Category(models.Model):
    category_name = models.CharField(
        max_length=100,
        default="No category",
        unique = True
    )


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
        on_delete=models.CASCADE
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


class PostCategory(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
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