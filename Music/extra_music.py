from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from django.core.files.base import ContentFile
import os


def extract_cover_from_file(music_instance):
    try:
        audio = MP3(music_instance.music_file.path, ID3=ID3)

        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                img_data = tag.data
                file_name = f"{music_instance.id}_cover.jpg"
                music_instance.cover_picture.save(file_name, ContentFile(img_data), save=False)
                music_instance.save(update_fields=['cover_picture'])
                break

    except Exception as e:
        print(f"Error: {e}")


def extra_data(music_instance):
    try:
        audio = MP3(music_instance.music_file.path, ID3=ID3)

        title = audio.tags.get("TIT2")
        artist = audio.tags.get("TPE1")

        if title and not music_instance.title:
            music_instance.title = title.text[0]

        if artist and not music_instance.artist_name:
            music_instance.artist_name = artist.text[0]

        music_instance.save(update_fields=['title', 'artist_name'])

    except Exception as e:
        print(f"Error reading extra metadata :  {e}")
