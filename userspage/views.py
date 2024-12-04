from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.auth import user_only
from . models import WatchList, UserProfile, Review
from . forms import ReviewForm
from app.models import MovieInfo,Genres
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models.functions import Lower
import os

def homepage(request):
    movies = MovieInfo.objects.all().order_by('-movieReleaseDate')[:8]
    reviews = Review.objects.all().order_by('rating')[:5]
    

    context={
        'movies': movies,
        'reviews':reviews,
        
    }
    return render(request,'client/homepage.html',context)


def movies(request):
    movies = MovieInfo.objects.all().order_by(Lower('movieTitle'))
    paginator = Paginator(movies, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        
        'page_obj':page_obj,
    }
    return render(request, 'client/movies.html',context)

def movieDetails(request,movieId):
    movie=MovieInfo.objects.get(id=movieId)
    genres = movie.genres.all()

    in_watchlist=False

    if request.user.is_authenticated:
        in_watchlist = WatchList.objects.filter(user=request.user, movie=movie).exists()

    recommended_movies = get_recommended_movies(movie, MovieInfo.objects.all())[:8]

    reviews=Review.objects.filter(movie=movie).order_by('-created_at')[:5]

    context={
        'movie':movie,
        'genres':genres,
        'reviews': reviews,
        'in_watchlist':in_watchlist,
        'recommended_movies':recommended_movies,
    }
    return render(request,'client/movieDetail.html',context)

def genres(request):
    genres = Genres.objects.all().order_by(Lower('genreName'))

    context={
        'genres':genres
    }
    return render(request,'client/genres.html',context)

def moviesByGenre(request,genreId):
    genre=Genres.objects.get(id=genreId)
    movies=MovieInfo.objects.filter(genres=genre).order_by(Lower('movieTitle'))

    paginator = Paginator(movies,8)

    page_number=request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={
        'genre':genre,
        'page_obj':page_obj
    }
    return render(request,'client/moviesByGenre.html',context)

@login_required
@user_only
def addToWatchList(request,movieId):
    movie= MovieInfo.objects.get(id=movieId)
    watch_list,created  = WatchList.objects.get_or_create(user=request.user,movie=movie)
    if created:
        messages.add_message(request,messages.SUCCESS,'Movie added to watchlist!')
    else:
        messages.add_message(request,messages.ERROR, 'Movie already in your watchlist!')

    return redirect('movie-detail',movieId=movie.id)

@login_required
@user_only
def removeFromWatchList(request,movieId):
    movie=MovieInfo.objects.get(id=movieId)
    watch_list = WatchList.objects.filter(user=request.user,movie=movie).first()
    if watch_list:
        watch_list.delete()
        messages.add_message(request,messages.SUCCESS,'Movie removed from watchlist!')
    else:
        messages.error(request,'Movie is not on your watchlist!')
    
    return redirect('watch-list')

@login_required
@user_only
def viewWatchList(request):
    watch_list = WatchList.objects.filter(user=request.user).select_related('movie')
    
    watch_list_with_ratings = []

    for item in watch_list:
        review = Review.objects.filter(user=request.user, movie=item.movie).first()
       
        watch_list_with_ratings.append({
            'movie': item.movie,
            'added_at': item.added_at,
            'rating': review.rating if review else None,
        })

    paginator = Paginator(watch_list_with_ratings, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={
        'page_obj':page_obj
    }
    return render(request, 'client/watchList.html',context)

@login_required
@user_only
def user_profile(request,username):
    user_profile = UserProfile.objects.get(user__username=username)
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    favorite_movies = user_profile.favorite_movies.all()
    
    review_paginator = Paginator(reviews,4)
    page_number = request.GET.get('page')
    page_obj = review_paginator.get_page(page_number)
    
    print(user_profile.userImage.url)
    context={
        'user_profile':user_profile,
        'page_obj':page_obj,
        'favorite_movies':favorite_movies,
        
    }
    return render(request,'client/userProfile.html',context)

@login_required
@user_only
def edit_profile_pic(request,username):
    user_profile = get_object_or_404(UserProfile,user__username=username)

    if request.method == 'POST':
        if request.FILES.get('userImage'):
            new_image = request.FILES['userImage']
            if os.path.exists(user_profile.userImage.path):
                os.remove(user_profile.userImage.path)

            
            user_profile.userImage = new_image
            user_profile.save()
            messages.success(request, "Profile image updated successfully!")

    return redirect('user-profile',username=username)

@login_required
@user_only
def edit_profile_bio(request,username):
    user_profile = get_object_or_404(UserProfile,user__username=username)

    if request.method == 'POST':
        if request.FILES.get('userImage'):
            new_bio = request.POST.get('bio')
            user_profile.bio = new_bio
            user_profile.save()
            messages.success(request, "Bio updated successfully!")

    return redirect('user-profile',username=username)

@login_required
@user_only
def add_to_favorites(request, movie_id):
    movie = MovieInfo.objects.get(id=movie_id)
    user_profile = request.user.userprofile

    if movie in user_profile.favorite_movies.all():
        messages.info(request, "Movie is already in your favorites.")
    else:
        user_profile.favorite_movies.add(movie)
        messages.success(request, "Movie added to favorites!")
        
    return redirect('movie-detail', movieId=movie_id)

@login_required
@user_only
def remove_from_favorites(request, movie_id):
    movie = MovieInfo.objects.get(id=movie_id)
    user_profile = request.user.userprofile

    if movie in user_profile.favorite_movies.all():
        user_profile.favorite_movies.remove(movie)
        messages.success(request, "Movie removed from favorites.")
    else:
        messages.info(request, "Movie was not in your favorites.")
        
    return redirect('movie-detail', movieId=movie_id)

def movie_search(request):
    query = request.GET.get('query','')
    results = MovieInfo.objects.filter(
        Q(movieTitle__icontains=query) |
        Q(movieDescription__icontains=query) |
        Q(genres__genreName__icontains=query)
    ).distinct()

    paginator = Paginator(results,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={
        'query':query,
        'page_obj':page_obj,
    }
    return render(request, 'client/search_result.html', context)

@login_required
@user_only
def add_review(request, movieId):
    movie = MovieInfo.objects.get(id=movieId)  # Corrected typo here
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        
        if request.user.is_authenticated:
            if rating and review_text:
                try:
                    rating = int(rating)  # Convert the rating to an integer
                    if rating < 1 or rating > 5:
                        raise ValueError("Rating must be between 1 and 5.")
                except ValueError:
                    messages.error(request, "Invalid rating. Please enter a number between 1 and 5.")
                    return render(request, 'movieDetail.html', {'movie': movie})

                existing_review = Review.objects.filter(movie=movie, user=request.user).first()
                if existing_review:
                    messages.error(request, "You have already reviewed this movie.")
                    return redirect('movie-detail', movieId=movieId)
                
                review = Review.objects.create(
                    movie=movie,
                    user=request.user,
                    rating=rating,
                    review_text=review_text
                )

                messages.success(request, "Review submitted successfully!")
                return redirect('movie-detail', movieId=movieId)  

            else:
                messages.error(request, "Please provide both rating and review text.")
        else:
            messages.error(request, "Please login to add reviews.")



@login_required
@user_only
def delete_review(request,review_id):
    review = Review.objects.get(id=review_id, user=request.user)

    review.delete()
    messages.error(request, "Review deleted.")
    return redirect('user-profile',username=request.user.username)

def get_recommended_movies(target_movie, all_movies):
    # Step 1: Retrieve genre IDs of the target movie
    target_genre_ids = set(target_movie.genres.values_list('id', flat=True))

    # Step 2: Initialize an empty list to store matching movies with scores
    matching_movies = []

    # Step 3: Perform linear search to calculate genre matches
    for movie in all_movies:
        if movie == target_movie:
            continue  # Skip the target movie itself

        # Retrieve genre IDs of the current movie
        movie_genre_ids = set(movie.genres.values_list('id', flat=True))

        # Calculate the number of shared genres (shortest "distance" logic)
        genre_match_count = len(target_genre_ids.intersection(movie_genre_ids))

        if genre_match_count > 0:
            # Add movie and its match count to the list
            matching_movies.append((movie, genre_match_count))

    # Step 4: Sort movies by genre match count (descending) and release date (descending)
    matching_movies.sort(key=lambda x: (-x[1], x[0].movieReleaseDate), reverse=False)

    # Step 5: Extract the sorted movies from the list of tuples
    recommended_movies = [movie for movie, _ in matching_movies]

    return recommended_movies




# def get_recommended_movies(genreId):
#     # Step 1: Retrieve all movies that have specified genre
#     movies_list = list(MovieInfo.objects.filter(genres__id=genreId))

#     # Step 2: Sort movies by release date in descending order using Bubble Sort
#     for i in range(len(movies_list)):
#         for j in range(0, len(movies_list) - i - 1):
#             if movies_list[j].movieReleaseDate > movies_list[j + 1].movieReleaseDate:
#                 # Swap if the release date of the current movie is greater than the next
#                 movies_list[j], movies_list[j + 1] = movies_list[j + 1], movies_list[j]

#     return movies_list





