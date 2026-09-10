from django import forms
from .models import Music, Album
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory

User = get_user_model()



class AlbumSelectForm(forms.Form):
    album = forms.ModelChoiceField(queryset=Album.objects.none(),
                                   label="انتخواب البم (اختیرای)",
                                   required=False,
                                   widget=forms.Select(attrs={'class':'form-control'}))
    def __init__(self, user,*args, **kwargs):
        super(AlbumSelectForm, self).__init__(*args, **kwargs)

        self.fields['album'].queryset = Album.objects.filter(user=user)



class CreateMusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ('music_file', 'genre')
        widgets = {
            'music_file': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'genre': forms.Select(attrs={'class':'form-control'}),
        }

MusicFormSet = inlineformset_factory(Album,Music, form=CreateMusicForm, extra=1, can_delete=True,)


class CreateAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('title', 'cover_album')



class SearchForm(forms.Form):
    query = forms.CharField()
