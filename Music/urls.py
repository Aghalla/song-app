from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'Music'

urlpatterns = [
    # Account
    path('Account/my_music', views.my_music, name='my_music'),
    path('Account/my_music/delete/<int:music_id>', views.delete_music, name='delete_music'),
    path('Account/my_playlist', views.my_playlist, name='my_playlist'),
    path('Account/my_playlist/delete/<int:album_id>', views.delete_album, name='delete_album'),
    path('Account/my_playlist/<int:album_id>', views.albums_music, name='albums_music'),
    path('Account/music/liks', views.music_liks, name='music_liks'),
    path('Account/album/save', views.albums_saves, name='album-like'),
    path('Account/follow/list', views.follow_user, name='follow_user'),

    #Musics
    path('', views.index, name='index'),
    path('musics', views.musics, name='musics'),
    path('musics/<str:genre_slug>', views.musics, name='musics_genre'),
    path('albums/', views.albums, name='albums'),
    path('albums/<int:album_id>', views.album_dtail, name='dtail-albums'),
    path("music/<int:music_id>/like/", views.toggle_like, name="toggle_like"),
    path("album/<int:album_id>/save/", views.saved_by, name="save-album"),
    path("music/<str:title_music>/<int:music_id>/", views.musics_detail, name="musics_detail"),
    path("profile/<str:username>", views.profile_username, name="profile-username"),

    #Add Musics
    path('Account/add/musics', views.add_music, name="add_music"),
    path('Account/add/albums', views.add_album, name="add_albums"),
    path('search/', views.sercher, name='search'),



]
