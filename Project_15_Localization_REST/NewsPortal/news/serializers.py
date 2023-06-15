from news.models import *
from rest_framework import serializers

class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "post_title"]