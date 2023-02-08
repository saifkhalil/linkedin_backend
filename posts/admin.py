from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin, register

from posts.models import post


@register(post)
class PostAdmin(ModelAdmin):
    icon_name = 'person'