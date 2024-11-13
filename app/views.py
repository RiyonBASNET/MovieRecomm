import os
from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import MovieInfo,Genres
from . forms import GenreForm, MovieForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.auth import admin_only, user_only
from django.core.paginator import Paginator


# Create your views here.

def index(rerquest):
    return HttpResponse('Help!!')

@login_required
@admin_only
def showMovies(request):
    movies = MovieInfo.objects.all().order_by('id')
    paginator = Paginator(movies,5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj,
    }

    return render(request,'demo/showMovies.html',context)

@login_required
@admin_only
def addGenre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Genre added')
            return redirect('/app/addGenre/')
        else:
            messages.add_message(request,messages.ERROR,'Error occured. Please check form fields')
            return render(request,'demo/addGenre.html',{
                'form': form
            })

    context={
        'form':GenreForm
    }

    return render(request,'demo/addGenre.html', context)

@login_required
@admin_only
def addMovie(request):
    if request.method =='POST':
        form = MovieForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Movie added')
            return redirect('/app/addMovie/')
        else:
            messages.add_message(request,messages.ERROR, 'Error. Please try again.')
            return render(request,'demo/addMovie.html',{
                'form':form
            })

    context = {
        'form':MovieForm
    }
    return render(request, 'demo/addMovie.html', context)

@login_required
@admin_only
def showGenres(request):
    genres = Genres.objects.all().order_by('genreName')

    paginator = Paginator(genres,5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj
    }

    return render(request,'demo/showGenres.html',context)

@login_required
@admin_only
def deleteGenre(request,genreId):
    id= int(genreId)
    genre=Genres.objects.get(id=id)
    genre.delete()
    messages.add_message(request,messages.SUCCESS,'Item deleted')
    return redirect('/app/genres')

@login_required
@admin_only
def updateGenreForm(request,genreId):
    genre= Genres.objects.get(id=genreId)
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Updated successfully!')
            return redirect('/app/genres')
        else:
            messages.add_message(request,messages.ERROR,'Could not delete item.Try again!')
            return render(request,'demo/updateGenre.html', {
                'form':form
            })
    
    context={
        'form':GenreForm(instance=genre)
    }

    return render(request,'demo/updateGenre.html',context)

@login_required
@admin_only
def deleteMovie(request,movieId):
    movie = MovieInfo.objects.get(id=movieId)
    os.remove(movie.image.path) 
    movie.delete()
    messages.add_message(request,messages.SUCCESS,'Item deleted successfully')
    return redirect('/app/movies')

@login_required
@admin_only
def updateMovieForm(request,movieId):
    movie = MovieInfo.objects.get(id=movieId)
    if request.method == 'POST':
        if request.FILES.get('movieImage'):
            os.remove(movie.movieImage.path)
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Updated successfully!')
            return redirect('/app/movies')
        else:
            messages.add_message(request,messages.ERROR,'Could not delete item.Try again!')
            return render(request,'demo/updateMovie.html', {
                'form':form
            })

    context={
        'form':MovieForm(instance=movie)
    }
    return render(request, 'demo/updateMovie.html', context)