from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from .forms import *
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from itertools import chain
import random


# Create your views here.


# ___________________Account
@login_required
def my_music(request):
    users_music = request.user.music
    music_list = users_music.all()

    context = {
        'music_list': music_list
    }

    return render(request, "UsersMusic/my_music.html", context)


@login_required
def delete_music(request, music_id):
    music = get_object_or_404(request.user.music, id=music_id)

    if request.method == "POST":
        music.delete()
    return redirect("Music:my_music")

@login_required
def delete_album(request, album_id):
    album = get_object_or_404(request.user.albums, id=album_id)
    if request.method == "POST":
        album.delete()

    return redirect("Music:my_playlist")


@login_required
def my_playlist(request):
    try:
        users_playlist = request.user.albums.all()
    except:
        users_playlist = []
    context = {
        'users_playlist': users_playlist
    }
    return render(request, 'UsersMusic/My_albums.html', context)


@login_required
def albums_music(request, album_id):
    album = get_object_or_404(Album, id=album_id, user=request.user)
    musics = album.musics.all()
    context = {
        'musics': musics,
        'album': album
    }
    return render(request, 'UsersMusic/albums_music.html', context)


@login_required
def music_liks(request):
    musics = Music.objects.filter(likes=request.user)

    context = {
        'musics': musics,
    }
    return render(request, 'UsersMusic/Musics-liks.html', context)


def albums_saves(request):
    albums = Album.objects.filter(saved_by=request.user)

    context = {
        'albums': albums,
    }
    return render(request, 'UsersMusic/albums-saves.html', context)



def follow_user(request):
    following = User.objects.filter(followers=request.user)
    context = {
        'following': following,
    }
    return render(request, 'UserOder/follow_user.html', context)
# _________________musics


def index(request):
    musics = Music.objects.all()[:10]
    albums = Album.objects.all()[:10]
    musics_popular = Music.objects.order_by("-totall_likes")[:15]
    user_popular = User.objects.order_by("followers")[:4]
    gener = Genre.objects.all()
    context = {
        'musics': musics,
        'albums': albums,
        "musics_popular": musics_popular,
        'user_popular': user_popular,
        'gener': gener,
    }

    return render(request, 'all_music/indext.html', context)


def musics(request, genre_slug=None):
    genre = None
    all_genres = Genre.objects.all()
    all_musics = Music.objects.all()

    if genre_slug:
        genre = get_object_or_404(Genre, slug=genre_slug)
        all_musics = Music.objects.filter(genre=genre)

    sort = request.GET.get('sort', "new")

    if sort == "old":
        all_musics = all_musics.order_by("created_at")
    elif sort == "new":
        all_musics = all_musics.order_by("-created_at")
    elif sort == "popular":
        all_musics = all_musics.order_by("-totall_likes")

    context = {
        'all_musics': all_musics,
        'all_genres': all_genres,
        'genre': genre
    }
    return render(request, 'all_music/music/more-music.html', context)


@login_required
def toggle_like(request, music_id):
    if request.method == "POST":

        music = get_object_or_404(Music, id=music_id)

        if request.user in music.likes.all():
            music.likes.remove(request.user)
            liked = False
        else:
            music.likes.add(request.user)
            liked = True

        music.totall_likes = music.likes.count()
        music.save()

        return JsonResponse({
            "liked": liked,
            "likes_count": music.totall_likes
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def saved_by(request, album_id):
    if request.method == "POST":
        album = get_object_or_404(Album, id=album_id)

        if request.user in album.saved_by.all():
            album.saved_by.remove(request.user)
            saved = False
        else:
            album.saved_by.add(request.user)
            saved = True

        return JsonResponse(
            {
                'saved': saved,
                'saved_count': album.saved_by.count()
            }
        )
    return JsonResponse({"error": "Invalid request"}, status=400)


def albums(request):
    albums = Album.objects.all()

    page_number = request.GET.get('page', 1)
    paginator = Paginator(albums, 12)
    page_obj = paginator.get_page(page_number)

    try:
        albums = paginator.page(page_number)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = []

    context = {
        'albums': albums,
        'page_obj': page_obj
    }

    return render(request, 'all_music/album/more-albums.html', context)


def album_dtail(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    musics = album.musics.all()

    context = {
        'musics': musics,
        'album': album
    }
    return render(request, 'all_music/album/dtail-albums.html', context)


def musics_detail(request, title_music, music_id):
    music = get_object_or_404(Music, id=music_id, title=title_music)

    # proposal
    proposal_gener = Music.objects.filter(genre=music.genre).exclude(id=music.id).all()[:9]
    artist_name = Music.objects.filter(artist_name=music.artist_name).exclude(id=music.id).all()[:9]
    uploder = Music.objects.filter(uploader=music.uploader).exclude(id=music.id).all()[:9]
    context = {
        'music': music,
        'proposal_gener': proposal_gener,
        'user_UP': uploder,
        'all_artist_name': artist_name,
    }
    return render(request, 'all_music/music/dtail-music.html', context)


def profile_username(request, username):
    user = get_object_or_404(User, username=username)
    musics_user = user.music.all()
    albums_user = user.albums.all()

    context = {
        'user': user,
        'musics_user': musics_user,
        'albums_user': albums_user
    }
    return render(request, 'UserOder/user_dtail.html', context)


def add_music(request):
    user = request.user

    if request.method == "POST":
        albums_form = AlbumSelectForm(user, request.POST)

        if albums_form.is_valid():
            selected_album = albums_form.cleaned_data.get('album')

            if selected_album:
                formset = MusicFormSet(request.POST, request.FILES, instance=selected_album)
            else:
                formset = MusicFormSet(request.POST, request.FILES)

            if formset.is_valid():
                musics = formset.save(commit=False)
                for music in musics:
                    music.uploader = user

                    if not selected_album:
                        music.album = None
                    music.save()

                formset.save_m2m()
                return redirect("profile:profile_index")
    else:
        albums_form = AlbumSelectForm(user=user)
        formset = MusicFormSet()

    return render(request, 'form/new_music.html', {"formset": formset, 'albums_form': albums_form})


def add_album(request):
    if request.method == "POST":
        albums_form = CreateAlbumForm(request.POST, request.FILES)

        if albums_form.is_valid():
            album = albums_form.save(commit=False)
            album.user = request.user
            album.save()
            return redirect("Music:add_music")
    else:
        albums_form = CreateAlbumForm()
    return render(request, 'form/new_album.html', {"albums_form": albums_form})


def sercher(request):
    query = None
    result_music = []
    results_user = []
    results_album = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            # MUSIC
            result_music1 = Music.objects.annotate(similarity=TrigramSimilarity("title", query)).filter(
                similarity__gt=0.1).order_by('-similarity')

            result_music2 = Music.objects.annotate(similarity=TrigramSimilarity("artist_name", query)).filter(
                similarity__gt=0.2).order_by('-similarity')

            result_music3 = Music.objects.annotate(similarity=TrigramSimilarity("album__title", query)).filter(
                similarity__gt=0.1).order_by('-similarity')

            result_music = (result_music1 | result_music2 | result_music3).order_by('-similarity')

            # USER
            results_user1 = User.objects.annotate(similarity=TrigramSimilarity("username", query)).filter(
                similarity__gt=0.3).order_by('-similarity')

            results_user2 = User.objects.annotate(similarity=TrigramSimilarity("first_name", query)).filter(
                similarity__gt=0.5).order_by('-similarity')

            results_user3 = User.objects.annotate(similarity=TrigramSimilarity("last_name", query)).filter(
                similarity__gt=0.5).order_by('-similarity')

            results_user = (results_user1 | results_user2 | results_user3).order_by('-similarity')

            # ALBUM
            results_album1 = Album.objects.annotate(similarity=TrigramSimilarity("title", query)).filter(
                similarity__gt=0.1).order_by('-similarity')

            results_album = results_album1.order_by('-similarity')

    results = chain(result_music, results_user, results_album)

    context = {
        'results': results,
        'query': query,
    }

    return render(request, 'serching.html', context)




