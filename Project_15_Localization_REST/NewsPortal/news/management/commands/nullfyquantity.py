from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError
from news.models import Post

class Command(BaseCommand):
    help = "Nullfy all likes"

    def handle(self, *args, **options):
        for post in Post.objects.all():
            post.post_rating = 0
            post.save()

            self.stdout.write(
                self.style.SUCCESS(
                     f"successfully nullify post id: {post.post_title}"
                )
            )