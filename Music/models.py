from django.db import models
from django.db.models import ForeignKey
from django.template.defaultfilters import title
from django_resized import ResizedImageField
from django.contrib.auth import get_user_model
from django_jalali.db import models as jmodels
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from .extra_music import *
from mutagen import File
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

User = get_user_model()


def upload_pic_to(instance, filename):
    album_name = slugify(instance.album.title) if instance.album else "no-album"
    username = slugify(instance.uploader.username)
    return f'{username}/pic/{album_name}/{filename}'


def upload_file_to(instance, filename):
    album_name = slugify(instance.album.title) if instance.album else "no-album"
    username = slugify(instance.uploader.username)
    return f'{username}/file/{album_name}/{filename}'


def upload_album_to(instance, filename):
    return f"{instance.user.username}/pic/albums/{filename}"


# --------------------------------


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=255)
    cover_album = models.ImageField(upload_to=upload_album_to, null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    saved_by = models.ManyToManyField(User, related_name='saved_albums', blank=True, related_query_name="سیو البوم")
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("Music:dtail-albums", args=[self.id])

    def delete(self, *args, **kwargs):
        if self.cover_album and self.cover_album.name:
            self.cover_album.delete(save=False)
        if self.cover_album and self.cover_album.name:
            self.cover_album.delete(save=False)

        super().delete(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def get_absolute_url(self):
        return reverse('Music:musics_genre', args=[self.slug])

    class Meta:
        ordering = ['-name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Music(models.Model):
    # genre = سبک موزیک

    # فارین کی ها
    album = ForeignKey(Album, on_delete=models.SET_NULL, related_name='musics', null=True, blank=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='music')

    title = models.CharField(max_length=120, verbose_name="عنوان", blank=True, null=True)
    artist_name = models.CharField(max_length=120, verbose_name="اسم هنرمند", blank=True, null=True)
    music_file = models.FileField(upload_to=upload_file_to,
                                  validators=[FileExtensionValidator(['mp3'])], verbose_name="فایل اهنگ")
    cover_picture = ResizedImageField(upload_to=upload_pic_to, size=[1600, 1600], quality=75, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, verbose_name="لایک ها")
    totall_likes = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=True)
    time = models.CharField(null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='musics', verbose_name='ژانر')

    # time
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.music_file:
            audio = File(self.music_file)
            length = int(audio.info.length)
            time_M = length // 60
            time_S = length % 60
            if time_S < 10:
                self.time = f"{time_M}:0{time_S}"
            else:
                self.time = f"{time_M}:{time_S}"


        super().save(*args, **kwargs)

        if not self.cover_picture and self.music_file:
            extract_cover_from_file(self)

        if not self.title or not self.artist_name and self.music_file:
            extra_data(self)

    def __str__(self):
        return f"{self.title}"

    def delete(self, *args, **kwargs):
        if self.music_file and self.music_file.name:
            self.music_file.delete(save=False)
        if self.cover_picture and self.cover_picture.name:
            self.cover_picture.delete(save=False)

        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse("Music:musics_detail", args=[self.title, self.id])
