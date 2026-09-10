from django.contrib import admin
from .models import *


# Register your models here.


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ["uploader", "title", "genre" ]
    list_filter = ["genre", "is_public"]



@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["id","title"]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]