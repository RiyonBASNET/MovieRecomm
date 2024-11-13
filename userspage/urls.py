from django.urls import path
from . import views

urlpatterns=[
    path('',views.homepage,name='homepage'),
    path('movies-list/',views.movies,name='movies-list'),
    path('movie/<int:movieId>/',views.movieDetails,name='movie-detail'),
    path('genres-list/',views.genres,name='genres-list'),
    path('genres/<int:genreId>/',views.moviesByGenre,name='movies-by-genre'),
    path('movie/<int:movieId>/add-to-watchlist/', views.addToWatchList, name='add-to-watchlist'),
    path('movie/<int:movieId>/remove-from-watchlist/', views.removeFromWatchList, name='remove-from-watchlist'),
    path('watchlist/', views.viewWatchList, name='watch-list'),
    path('profile/<str:username>/',views.user_profile,name='user-profile'),
    path('edit-profile-pic/<str:username>/',views.edit_profile_pic,name='edit-profile-pic'),
    path('edit-profile-bio/<str:username>/',views.edit_profile_bio,name='edit-profile-bio'),
    path('favorite/add/<int:movie_id>/', views.add_to_favorites, name='add-to-favorites'),
    path('favorite/remove/<int:movie_id>/', views.remove_from_favorites, name='remove-from-favorites'),
    path('search/',views.movie_search,name='movie-search'),
    path('add-review/<int:movieId>/',views.add_review,name='add-review'),
    path('delete-review/<int:review_id>/',views.delete_review,name='delete-review'),

]