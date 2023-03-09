from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    rating = models.IntegerField(
        default=0
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    def update_rating(self):
        from news.models import (
            Post,
            Comment
        )

        articles_rating = 0
        articles = Post.objects.filter(
            post_type=Post.article,
            author_id=self.id
        )
        if articles:
            for article in articles:
                articles_rating += article.post_rating

        author_comments_rating = 0
        author_comments = Comment.objects.filter(
            user_id=self.id
        )
        if author_comments:
            for author_comment in author_comments:
                author_comments_rating += author_comment.comment_rating

        post_comments_rating = 0
        posts = Post.objects.filter(
            author_id=self.id
        )
        if posts:
            for post_object in posts:
                post_comments = Comment.objects.filter(
                    post_id=post_object.id
                )
                if post_comments:
                    for comment in post_comments:
                        post_comments_rating += comment.comment_rating

        self.rating = articles_rating * 3 + author_comments_rating + post_comments_rating
        self.save()

        return self.rating