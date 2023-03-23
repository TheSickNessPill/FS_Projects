from django import forms
from django.core.exceptions import ValidationError

from news.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "post_title",
            "post_text",
            "post_rating",
            "author"
        ]

    def clean(self):
        cleaned_data = super().clean()

        post_text = cleaned_data.get("post_text")
        if post_text is not None and len(post_text) < 20:
            raise ValueError({
                "post_text": "Текст меньше 20ти символов",
            })

        post_title = cleaned_data.get("post_title")
        if post_title == post_text:
            raise ValidationError(
                "Описание не должно быть идентично названию"
            )
        return cleaned_data