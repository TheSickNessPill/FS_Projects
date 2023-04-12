from django.forms import DateInput
import django_filters
from django_filters import FilterSet
from news.models import Post
# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики

class PostFilter(FilterSet):
    post_create_datetime = django_filters.DateFilter(
        lookup_expr="gt",
        field_name="post_create_datetime",
        widget = DateInput(
            attrs={
                "class": "form-control",
                'type': 'date'
            }
        )
    )
    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'post_title': ['icontains'],
            'post_category': ['exact'],
            # количество товаров должно быть больше или равно
            'post_rating': ['exact'],
        }