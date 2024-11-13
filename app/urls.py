from django.urls import path
from  . import views


urlpatterns=[
    path('movies/',views.showMovies,name='admin-movies-list'),
    path('addGenre/',views.addGenre,name='add-genre'),   
    path('addMovie/',views.addMovie,name='add-movie'),
    path('genres/',views.showGenres,name='admin-genres-list'),
    path('deleteGenre/<int:genreId>/',views.deleteGenre, name='delete_genre'),
    path('updateGenre/<int:genreId>/',views.updateGenreForm, name='edit_genre'),
    path('deleteMovie/<int:movieId>/',views.deleteMovie,name='delete_movie'),
    path('updateMovie/<int:movieId>/',views.updateMovieForm,name='edit_movie'),
    
]

