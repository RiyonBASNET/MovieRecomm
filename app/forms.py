from django.forms import ModelForm
from . models import Genres,MovieInfo

class GenreForm(ModelForm):
    class Meta:
        model=Genres
        fields='__all__'

class MovieForm(ModelForm):
    class Meta:
        model=MovieInfo
        fields=['movieTitle','movieReleaseDate','movieDescription','image','trailerUrl','genres',]