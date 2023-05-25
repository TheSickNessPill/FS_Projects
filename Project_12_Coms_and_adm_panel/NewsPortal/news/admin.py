from django.contrib import admin
from news.models import Post, Category

def set_rating_one(modeladmin, request, queryset):
    queryset.update(post_rating=1)
set_rating_one.short_description = "Устаносить везде 1"

class PostAdmin(admin.ModelAdmin):
    list_display = ("post_title", "post_type", "category", "post_rating")
    list_filter = ("post_title", "category")
    search_fields = ["post_title"]
    actions = [set_rating_one]

admin.site.register(Category)
admin.site.register(Post, PostAdmin)

admin.site.unregister(Category)